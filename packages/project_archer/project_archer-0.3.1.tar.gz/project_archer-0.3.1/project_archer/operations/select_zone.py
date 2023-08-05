from project_archer.environment.environment import BashEnvironment


def select_zone(args, env: BashEnvironment):
    env.set_envvar(
        "CIPLOGIC_ARCHER_CURRENT_" + args.internalRunMode.upper() + "_ZONE", args.zone
    )
    env.flush()
