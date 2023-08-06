# This file is part of Marcel.
# 
# Marcel is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or at your
# option) any later version.
# 
# Marcel is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Marcel.  If not, see <https://www.gnu.org/licenses/>.

import threading

import marcel.argsparser
import marcel.core
import marcel.exception
import marcel.opmodule
import marcel.object.cluster
import marcel.op.labelthread
import marcel.op.remote

HELP = '''
{L,wrap=F}fork HOST PIPELINE
{L,wrap=F}fork N PIPELINE

{L,indent=4:28}HOST                    The name of the host or set of hosts on which to run the given PIPELINE.

{L,indent=4:28}N                       The number of instances of the PIPELINE to run locally (and concurrently).

{L,indent=4:28}PIPELINE                The PIPELINE to be executed.

Run multiple copies of a pipeline, concurrently, usually on remote hosts.

If the first argument is a {r:HOST}, then the 
{r:PIPELINE} is run on the specified {r:HOST}. The {r:HOST} must have been configured in
the marcel configuration file. (Note that {r:HOST} may identify one or more hosts.)

If the first argument is {r:N}, then the {r:PIPELINE} is run the specified
number of times, concurrently.

The output will contain the tuples obtained by running the command. The first
element of each tuple will either identify the host, or be a number between
0 and {r:N}-1.
For example, if the cluster named {n:lab} contains hosts {n:192.168.0.100},
and {n:198.169.0.101}, then this command:

{L}@lab [ gen 3 ]

will generate this output (possibly reordered):

{p,indent=4,wrap=F}
('192.168.0.100', 0)
('192.168.0.100', 1)
('192.168.0.100', 2)
('192.168.0.101', 0)
('192.168.0.101', 1)
('192.168.0.101', 2)

This command:

{L}@2 [ gen 3 ]

will generate this output (possibly reordered):

{p,indent=4,wrap=F}
(0, 0)
(0, 1)
(0, 2)
(1, 0)
(1, 1)
(1, 2)
'''


def fork(env, host, pipelineable):
    assert isinstance(pipelineable, marcel.core.Pipelineable)
    pipelineable = pipelineable.create_pipeline()
    return Fork(env), [host, pipelineable]


class ForkArgsParser(marcel.argsparser.ArgsParser):

    def __init__(self, env):
        super().__init__('fork', env)
        self.add_anon('host', convert=self.fork_spec)
        self.add_anon('pipeline', convert=self.check_pipeline)
        self.validate()


class Fork(marcel.core.Op):

    def __init__(self, env):
        super().__init__(env)
        self.host = None  # TODO: Actually a fork spec. Improve terminology.
        self.pipeline = None
        self.thread_labels = None
        self.threads = None
        self.impl = None

    def __repr__(self):
        return f'fork({self.host}, {self.pipeline})'

    # AbstractOp

    def setup_1(self, env):
        super().setup_1(env)
        self.host = self.eval_function('host', int, str)
        self.threads = []
        cluster = self.host if type(self.host) is marcel.object.cluster.Cluster else env.cluster(self.host)
        if cluster:
            self.impl = Remote(self, cluster)
        elif isinstance(self.host, int):
            # Number of threads, from API
            self.impl = Local(self, self.host)
        elif self.host.isdigit():
            # Number of threads, from console
            self.impl = Local(self, int(self.host))
        else:
            raise marcel.exception.KillCommandException(f'Invalid fork specification: {self.host}')
        self.impl.setup_1(env)

    def setup_2(self, env):
        self.impl.setup_2(env)

    def set_env(self, env):
        self.impl.set_env(env)

    def receive(self, _):
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            while thread.isAlive():
                try:
                    thread.join(0.1)
                except BaseException as e:
                    thread.terminating_exception = e
        # Threads may complete normally or fail with a variety of exceptions. Merge them into a single action
        # for the termination of the fork op.
        kill_command = None
        kill_and_resume = None
        ctrl_c = None
        for thread in self.threads:
            e = thread.terminating_exception
            if e:
                if isinstance(e, marcel.exception.KillAndResumeException):
                    kill_and_resume = e
                elif isinstance(e, KeyboardInterrupt):
                    ctrl_c = e
                else:
                    kill_command = e
        if kill_command:
            raise marcel.exception.KillCommandException(kill_command)
        if ctrl_c:
            raise KeyboardInterrupt()
        if kill_and_resume:
            self.fatal_error(None, str(kill_and_resume))

    # Op

    def must_be_first_in_pipeline(self):
        return True

    # For use by this class

    @staticmethod
    def attach_thread_label(op, thread_label):
        if isinstance(op, marcel.op.labelthread.LabelThread):
            op.set_label(thread_label)
        elif isinstance(op, marcel.op.remote.Remote):
            op.set_host(thread_label)


class ForkImplementation:
    
    def __init__(self, op):
        self.op = op
        
    def setup_1(self, env):
        self.generate_thread_labels(env)

    def setup_2(self, env):
        assert False

    def set_env(self, env):
        for thread in self.op.threads:
            thread.set_env(env)

    def generate_thread_labels(self, env):
        assert False


class Remote(ForkImplementation):

    def __init__(self, op, cluster):
        super().__init__(op)
        self.cluster = cluster

    # AbstractOp

    def setup_1(self, env):
        super().setup_1(env)
        op = self.op
        remote_pipeline = marcel.core.Pipeline()
        remote_pipeline.append(marcel.opmodule.create_op(env, 'remote', self.op.pipeline))
        remote_pipeline.append(marcel.op.labelthread.LabelThread(None))
        op.pipeline = remote_pipeline
        # Don't set the LabelThread receiver here. We don't want the receiver cloned,
        # we want all the cloned pipelines connected to the same receiver.

    def setup_2(self, env):
        op = self.op
        for thread_label in op.thread_labels:
            pipeline_copy = op.pipeline.copy()
            pipeline_copy.set_error_handler(op.owner.error_handler)
            # Attach thread label to Remote op.
            remote_op = pipeline_copy.first_op
            assert isinstance(remote_op, marcel.op.remote.Remote)
            remote_op.set_host(thread_label)
            # Attach thread label to LabelThread op.
            label_thread_op = pipeline_copy.last_op
            assert isinstance(label_thread_op, marcel.op.labelthread.LabelThread)
            label_thread_op.set_label(thread_label)
            # DON'T do setup_1 here. The pipeline is going to run remotely, so setup is done remotely.
            # Connect receivers
            remote_op.receiver = label_thread_op
            label_thread_op.receiver = op.receiver
            # Create a thread to run the pipeline copy
            op.threads.append(PipelineThread(thread_label, pipeline_copy))

    # Subclass

    def generate_thread_labels(self, env):
        self.op.thread_labels = [host for host in self.cluster.hosts]


class Local(ForkImplementation):

    def __init__(self, op, n):
        super().__init__(op)
        self.n = n

    # AbstractOp

    def setup_1(self, env):
        super().setup_1(env)
        op = self.op
        op.pipeline.append(marcel.op.labelthread.LabelThread(None))
        # Don't set the LabelThread receiver here. We don't want the receiver cloned,
        # we want all the cloned pipelines connected to the same receiver.

    def setup_2(self, env):
        op = self.op
        for thread_label in op.thread_labels:
            # Copy the pipeline
            pipeline_copy = op.pipeline.copy()
            pipeline_copy.set_error_handler(op.owner.error_handler)
            # Attach thread label to LabelThread op.
            label_thread_op = pipeline_copy.last_op
            assert isinstance(label_thread_op, marcel.op.labelthread.LabelThread)
            label_thread_op.set_label(thread_label)
            pipeline_copy.setup_1(env)
            # Connect LabelThread op to receiver
            label_thread_op.receiver = op.receiver
            # Create a thread to run the pipeline copy
            op.threads.append(PipelineThread(thread_label, pipeline_copy))

    # Subclass

    def generate_thread_labels(self, env):
        self.op.thread_labels = [x for x in range(self.n)]


class PipelineThread(threading.Thread):

    def __init__(self, thread_label, pipeline_copy):
        super().__init__()
        self.thread_label = thread_label
        self.pipeline = pipeline_copy
        self.terminating_exception = None

    def __repr__(self):
        return f'PipelineThread({self.thread_label})'

    def set_env(self, env):
        self.pipeline.set_env(env)

    def run(self):
        try:
            self.pipeline.receive(None)
            self.pipeline.receive_complete()
        except BaseException as e:
            self.terminating_exception = e
