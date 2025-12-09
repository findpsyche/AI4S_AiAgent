"""
Redis缓存服务
Cache Service with Redis
"""

import logging
import json
from typing import Any, Optional
import redis.asyncio as redis

from app.config import settings

logger = logging.getLogger(__name__)


class CacheService:
    """Redis缓存服务"""
    
    def __init__(self):
        self.settings = settings
        self.redis_client = None
        self.logger = logger
    
    async def connect(self):
        """连接Redis"""
        try:
            self.redis_client = await redis.Redis(
                host=self.settings.REDIS_HOST,
                port=self.settings.REDIS_PORT,
                db=self.settings.REDIS_DB,
                password=self.settings.REDIS_PASSWORD,
                decode_responses=True
            )
            
            # 测试连接
            await self.redis_client.ping()
            self.logger.info("✅ Redis连接成功")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Redis连接失败: {str(e)}")
            self.redis_client = None
    
    async def disconnect(self):
        """断开Redis连接"""
        if self.redis_client:
            await self.redis_client.close()
            self.logger.info("Redis已断开连接")
    
    async def get(self, key: str) -> Optional[Any]:
        """从缓存获取数据"""
        if not self.redis_client:
            return None
        
        try:
            data = await self.redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            self.logger.warning(f"缓存get错误 {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存"""
        if not self.redis_client:
            return False
        
        try:
            ttl = ttl or self.settings.REDIS_TTL
            await self.redis_client.setex(
                key,
                ttl,
                json.dumps(value, default=str)
            )
            return True
        except Exception as e:
            self.logger.warning(f"缓存set错误 {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self.redis_client:
            return False
        
        try:
            await self.redis_client.delete(key)
            return True
        except Exception as e:
            self.logger.warning(f"缓存delete错误 {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if not self.redis_client:
            return False
        
        try:
            return await self.redis_client.exists(key) > 0
        except Exception as e:
            self.logger.warning(f"缓存exists错误 {key}: {e}")
            return False
    
    async def clear_all(self):
        """清空所有缓存"""
        if not self.redis_client:
            return False
        
        try:
            await self.redis_client.flushdb()
            return True
        except Exception as e:
            self.logger.warning(f"缓存清空错误: {e}")
            return False
