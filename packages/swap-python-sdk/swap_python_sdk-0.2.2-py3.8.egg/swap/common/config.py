from environs import Env


env = Env()


class Settings:
    BUCKET = env.str('BUCKET', 'bucket-name')
    DAS_URL = env.str('DAS_URL', 'https://das.stage.swap.akerbp.com')
    LOG_LEVEL = env.str('LOG_LEVEL', 'INFO')
    SERVICE_DISCOVERY_URL = env.str('SERVICE_DISCOVERY_URL', 'https://service-discovery.stage.swap.akerbp.com')
    SWAP_API_TOKEN = env.str('SWAP_API_TOKEN')
    UBL_URL = env.str('UBL_URL', 'https://ubl.stage.swap.akerbp.com')
