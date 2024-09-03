from configparser import ConfigParser
from argparse import ArgumentParser


def init_config():
    config_argparse = ArgumentParser(prog=__file__, add_help=False)
    config_argparse.add_argument('-c', '--config-file',
                                 default='app.conf',
                                 help='path to configuration file')
    config_args, _ = config_argparse.parse_known_args()

    config_parser = ConfigParser()
    config_parser.read(config_args.config_file)
    defaults = dict(config_parser.items('POSTGRES'))
    parsers = [config_argparse]

    main_parser = ArgumentParser(
        parents=parsers
    )
    main_parser.set_defaults(**defaults)
    main_parser.add_argument('filename')
    # positional argument
    main_parser.add_argument('-U', '--pguser',)
    main_parser.add_argument('-W', '--pgpasswd')
    main_parser.add_argument('-H', '--pghost')
    main_parser.add_argument('-P', '--pgport')
    main_parser.add_argument('-D', '--database')
    main_args = main_parser.parse_args()
    config = vars(main_args)
    config['DB_URI'] = f"postgresql+asyncpg://{main_args.pguser}:{main_args.pgpasswd}@{main_args.pghost}:{main_args.pgport}/{main_args.database}"
    return config

config = init_config()
