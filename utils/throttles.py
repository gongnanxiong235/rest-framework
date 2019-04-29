from rest_framework.throttling import SimpleRateThrottle


class IPThrottles(SimpleRateThrottle):
    # 配置文件中的key,可以自定义 和配置文件保持一致即可
    scope = 'gnx'

    # 配置按照什么进行节流，get_ident(request)是获取IP地址  也可以自定义 其他  如user_id等
    def get_cache_key(self, request, view):
        return self.get_ident(request)
