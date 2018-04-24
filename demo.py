from lnt import SafetyWrapper
import argparse
from env_util import get_env
from coach_util import Agent


def learn_safely(env_name, safety_param, output_dir):
    (env, lnt_params, agent_params) = get_env(env_name, safety_param)

    # 1. Create a reset agent that will reset the environment
    reset_agent = Agent(env, name='reset_agent', **agent_params)

    # 2. Create a wrapper around the environment to protect it
    safe_env = SafetyWrapper(env=env, reset_agent=reset_agent, **lnt_params)

    # 3. Safely learn to solve the task.
    Agent(env=safe_env, name='forward_agent', **agent_params).improve()

    # Plot the reward and resets throughout training
    safe_env.plot_metrics(output_dir)

def learn_dangerously(env_name):
    (env, _, agent_params) = get_env(env_name)
    Agent(env, name='agent', **agent_params).improve()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Let\'s do safe RL with Leave No Trace!')
    env_list = ['small-gridworld', 'large-gridworld', 'hopper', 'cheetah']
    parser.add_argument('--env_name', type=str, default='FrozenLake-v0',
                        help=('Name of the environment. The currently supported '
                              'environments are: %s') % env_list)
    parser.add_argument('--safety_param', type=float, default=0.3,
                        help=('Increasing the safety_param from 0 to 1 makes the '
                              'agent safer. A reasonable value is 0.3'))
    parser.add_argument('--output_dir', type=str, default='/tmp',
                        help='Folder for storing results')
    parser.add_argument('--learn_safely', type=bool, default=True,
                        help=('Whether to learn safely using '
                              'Leave No Trace'))
    args = parser.parse_args()
    assert 0 < args.safety_param < 1, 'The safety_param should be between 0 and 1.'
    if args.learn_safely:
        learn_safely(args.env_name, args.safety_param,
                     args.output_dir)
    else:
        learn_dangerously(args.env_name)
