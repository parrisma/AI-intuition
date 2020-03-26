import unittest
import threading
import random
import time
from pubsub import pub
from journey11.interface.task import Task
from journey11.interface.taskpool import TaskPool
from journey11.test.task.testtask import TestTask
from journey11.lib.state import State
from journey11.lib.simpletaskpool import SimpleTaskPool
from journey11.lib.simpleworkinitiate import SimpleWorkInitiate
from journey11.test.agent.testagent import TestAgent


class Listener:
    _id = 0

    def __init__(self):
        self.name = str(Listener._id)
        Listener._id += 1

    def __call__(self, arg1):
        print("{} Rx Msg {}".format(self.name, type(arg1)))
        return


class TestTheTaskPool(unittest.TestCase):

    def test_single_task_scenarios(self):

        # [task_effort, agent_capacity, num_tasks, num_agents]
        scenarios = [[1, 1, 1, 1, State.S0, State.S1],
                     [2, 1, 1, 1, State.S0, State.S1],
                     [2, 2, 1, 1, State.S0, State.S1],
                     [2, 4, 1, 1, State.S0, State.S1],
                     [4, 2, 25, 1, State.S0, State.S1],
                     [8, 2, 33, 10, State.S0, State.S1],
                     [100, 1, 1, 1, State.S0, State.S1]]

        scenarios = [[1, 1, 1, 5, State.S0, State.S8]]

        case_num = 1
        for task_effort, agent_capacity, num_tasks, num_agents, start_state, end_state in scenarios:
            case_description \
                = "Case {}: Effort={}, Capacity={}, Tasks={}, Agents={} Start={}, End={}".format(case_num,
                                                                                                 task_effort,
                                                                                                 agent_capacity,
                                                                                                 num_tasks,
                                                                                                 num_agents,
                                                                                                 start_state,
                                                                                                 end_state)
            self.test_scenario_execute(case_description,
                                       task_effort,
                                       agent_capacity,
                                       num_tasks,
                                       num_agents,
                                       start_state,
                                       end_state)
            case_num += 1
        return

    def test_scenario_execute(self,
                              case_descr: str,
                              task_effort: int,
                              agent_capacity: int,
                              num_tasks: int,
                              num_agents: int,
                              start_state: State,
                              end_state: State) -> None:
        """
        Add a singls task to pool and then get it.
        Verify the task count on the pool at all stages and ensure that the task returned is the same as the
        task injected.
        """

        print("\n* * * * * * S T A R T: {} * * * * * * \n".format(case_descr))

        TestTask.global_sync_reset()

        # Tasks: Single state transition
        TestTask.process_start_state(start_state)
        TestTask.process_end_state(end_state)

        # Init task pool
        task_pool = SimpleTaskPool('Task Pool 1')

        # Create Agents
        agents = list()
        st = start_state
        i = 1
        for es in State.range(start_state, end_state)[1:]:
            for _ in range(num_agents):
                agent = TestAgent(agent_name="Agent {}".format(i),
                                  start_state=st,
                                  end_state=es,
                                  capacity=agent_capacity)
                agents.append(agent)
                i += 1
            st = es

        # Must create all agents *before* subscription - otherwise odd effect where only last agent listens.
        for agent in agents:
            pub.subscribe(agent, topicName=task_pool.topic_for_state(agent.from_state))

        # Create tasks
        tasks = list()
        work_init = list()
        for _ in range(num_tasks):
            t = TestTask(effort=task_effort, start_state=State.S0)
            tasks.append(t)
            work_init.append(SimpleWorkInitiate(t))

        for w in work_init:
            pub.sendMessage(topicName=task_pool.topic, arg1=w)

        # Wait for all tasks to report arrival in terminal state
        TestTask.global_sync_wait()

        # Validate behaviours for this test case
        #
        for agent in agents:
            self.assertEqual(num_tasks, agent.num_notification)

        num_transitions = len(State.range(start_state, end_state)) - 1
        self.assertEqual(0, len(task_pool))
        for t in tasks:
            self.assertEqual(end_state, t.state)
            self.assertEqual(max(1, int(task_effort / agent_capacity) * num_transitions), t.lead_time)

        task_pool.terminate_all()

        print("\n* * * * * * E N D : {} * * * * * * \n".format(case_descr))

        return

    @unittest.skip
    def test_multi_task_multi_state(self) -> None:
        """
        add multiple tasks in different states and then get them
        Verify the the task pool count at all stages and that the tasks returned in the gat are the same
        as the tasks added.
        """
        test_task1 = TestTask(effort=1, start_state=State.S0)
        test_task2 = TestTask(effort=1, start_state=State.S0)
        test_task3 = TestTask(effort=1, start_state=State.S1)
        test_task4 = TestTask(effort=1, start_state=State.S1)
        test_task5 = TestTask(effort=1, start_state=State.S2)

        tasks = [test_task1, test_task2, test_task3, test_task4, test_task5]

        task_pool = SimpleTaskPool('Task Pool 2')

        self.assertEqual(len(task_pool), 0)
        for t in tasks:
            res0 = task_pool.get_task(t)
            self.assertIsNone(res0)
        print(task_pool)

        i = 0
        for t in tasks:
            task_pool.put_task(t)
            i += 1
            self.assertEqual(len(task_pool), i)
        print(task_pool)

        i = 5
        for t in tasks:
            res1 = task_pool.get_task(t)
            i -= 1
            self.assertEqual(len(task_pool), i)
            self.assertEqual(id(t), id(res1))
        print(task_pool)

        for t in tasks:
            res2 = task_pool.get_task(t)
            self.assertIsNone(res2)
        return

    #
    # Threaded Test Utility Class
    #
    class TaskGetter(unittest.TestCase):
        """
        Delayed timer action that will wait on a given Event and then get the given task from the pool
        Verify the task returned is the same as the task added.
        """

        def __init__(self,
                     name: str,
                     task_pool: TaskPool,
                     task: Task,
                     lock: threading.Event):
            super().__init__()
            self._task_pool = task_pool
            self._task = task
            self._lock = lock
            self._name = name
            return

        def __call__(self, *args, **kwargs):
            print("Getter {} waiting".format(self._name))
            self._lock.wait()
            print("Getter {} running".format(self._name))
            res = self._task_pool.get_task(self._task)
            self.assertEqual(id(self._task), id(res))
            print("Getter {} done".format(self._name))

            pass

    @unittest.skip
    def test_threaded_test(self) -> None:
        """
        Verify the behaviour and integrity of the pool when in an async threaded set-up.
        Add 100 tasks of random states to the pool aor each task create a timer action with a random 0 to 1 sec
        delay that will get the same task from the pool.
        Verify the task count as tasks are injected and that task count in pool is zero when all threads are done.
        In the timer callback get the task and ensure it has same object id as the task added - we know what the added
        task was as it is given to the timer call back object.
        :return:
        """
        task_pool = SimpleTaskPool('Task Pool 3')
        lock = threading.Event()
        lock.clear()

        # Add random tasks
        #
        states = [State.S0, State.S1, State.S2, State.S3, State.S4, State.S5, State.S5, State.S7, State.S8, State.S9]
        tasks = list()
        for i in range(100):
            t = TestTask(effort=1, start_state=random.choice(states))
            tasks.append(t)
            task_pool.put_task(t)
            self.assertEqual(len(task_pool), i + 1)

        print(task_pool)

        i = 1
        for t in tasks:
            timer_action = TestTheTaskPool.TaskGetter(str(i), task_pool, t, lock)
            i += 1
            threading.Timer(0.5 + random.random(), timer_action).start()

        lock.set()  # Release all the queued timer threads.
        time.sleep(2)

        self.assertEqual(len(task_pool), 0)
        for t in tasks:
            res = task_pool.get_task(t)
            self.assertIsNone(res)
        return

    @unittest.skip
    def test_pub_sub_state_chain(self) -> None:
        """
        Test the pub/sub cycle where tasks advance through a state sequence
        0. Agents are created for state transitions S0 - S1, S1 - S2 etc and listen to pool on these topics
        1. Task added in state S0
        2. TaskPool advertises task on S0 topic
        3. Agent that can work on S0 is notified via Topic
        4. Agent calls a Get() on the task from the TaskPool
        4.1 Sometimes agent will not consume as it is 'busy' this requires the pool to re-advertises tasks not consumed
        5. Agent does work to get task from S0 to S1
        6. Agent adds task in now in state S1 back to the pool
        7. Task Pool task on S2 topic
        8. Agent that can work on S0 is notified via Topic
        9. ..... S1, S2, S3 ... S-terminal-state
        10. Agent does work to get task from S-n to S-terminal-state
        11. Tasks in S-terminal-state are noted to the pool and process ends.
        """

        # Scenario
        #
        pool_name = "Task Pool 4"

        # Agent: [From State, To State],[Num agents per State (topic), Agent Capacity (to do work)]
        test_agents = [[[State.S0, State.S1], [10, 1]],
                       [[State.S1, State.S2], [10, 2]],
                       [[State.S2, State.S3], [10, 1]],
                       [[State.S3, State.S4], [1, 4]],
                       [[State.S4, State.S5], [1, 1]],
                       [[State.S5, State.S6], [1, 2]]
                       ]
        te = 4  # Task Effort
        test_tasks = [500, te, State.S0, (te / 1 + te / 2 + te / 1 + te / 4 + te / 1 + te / 2)]

        # Set overall start end terminal states
        #
        TestTask.process_start_state(test_agents[0][0][1])
        TestTask.process_end_state(test_agents[-1][0][-1])

        # Create the task pool
        #
        task_pool = SimpleTaskPool(pool_name)

        # Create agents
        #
        agents = list()
        for state, agent_settings in test_agents:
            num_agents_per_state, capacity = agent_settings
            for i in range(num_agents_per_state):
                agent_name = "Agent-{}-{}".format(str(state[0]), i)
                agent = TestAgent(agent_name=agent_name, start_state=state[0], end_state=state[1], capacity=capacity)
                agents.append(agent)
                pub.subscribe(agent, task_pool.topic_for_state(state[0]))

        TestTask.global_sync_reset()

        tasks = list()
        num_tasks, task_effort, start_st, expected_lead_time = test_tasks
        for _ in range(num_tasks):
            t = TestTask(effort=task_effort, start_state=start_st)
            task_pool.put_task(t)
            tasks.append(t)

        TestTask.global_sync_wait()
        time.sleep(5)

        print(task_pool)

        # Check all tasks have expected lead time
        for t in tasks:
            self.assertEqual(expected_lead_time, t.lead_time)

        # Check task pool is empty
        self.assertEqual(len(task_pool), 0)
        for t in tasks:
            res = task_pool.get_task(t)
            self.assertIsNone(res)


if __name__ == "__main__":
    unittest.main()
