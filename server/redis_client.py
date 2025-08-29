import os
import logging
import redis
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client wrapper with connection management and utility methods."""

    def __init__(self):
        self.client: Optional[redis.Redis] = None
        self.available: bool = False

        # Get Redis configuration from environment variables
        self.host: str = os.environ.get("REDIS_HOST", "localhost")
        self.port: int = int(os.environ.get("REDIS_PORT", 6379))

        # Try initial connection
        self.connect()

    def connect(self) -> bool:
        """Establish Redis connection with retry logic."""
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=0,
                decode_responses=True,
                socket_connect_timeout=10,
                socket_timeout=10,
                retry_on_timeout=True,
            )
            # Test the connection
            self.client.ping()
            self.available = True
            logger.info(
                f"Redis connection established successfully at {self.host}:{self.port}"
            )
            return True
        except (redis.ConnectionError, redis.TimeoutError) as e:
            logger.warning(f"Redis connection failed: {e}")
            self.available = False
            return False
        except Exception as e:
            logger.error(f"Unexpected Redis error: {e}")
            self.available = False
            return False

    def get(self, key: str) -> Optional[str]:
        """Get value from Redis cache."""
        if not self.available or not self.client:
            return None

        try:
            return self.client.get(key)
        except Exception as e:
            logger.warning(f"Redis get error for key {key}: {e}")
            return None

    def setex(self, key: str, time: int, value: str) -> bool:
        """Set value in Redis cache with expiration."""
        if not self.available or not self.client:
            return False

        try:
            self.client.setex(key, time, value)
            return True
        except Exception as e:
            logger.warning(f"Redis setex error for key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from Redis cache."""
        if not self.available or not self.client:
            return False

        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Redis delete error for key {key}: {e}")
            return False

    def ping(self) -> bool:
        """Test Redis connection."""
        if not self.available or not self.client:
            return False

        try:
            return self.client.ping()
        except Exception as e:
            logger.warning(f"Redis ping error: {e}")
            self.available = False
            return False

    def test_connection(self) -> Dict[str, Any]:
        """Test Redis connection and basic operations."""
        if not self.available:
            return {"status": "error", "message": "Redis not available"}

        try:
            # Test basic operations
            test_key = "test:cache:ping"
            test_value = "pong"

            # Set a test value
            if not self.setex(test_key, 60, test_value):
                return {"status": "error", "message": "Failed to set test value"}

            # Get the test value
            retrieved_value = self.get(test_key)
            if retrieved_value != test_value:
                return {
                    "status": "error",
                    "message": "Redis read/write test failed",
                    "expected": test_value,
                    "got": retrieved_value,
                }

            # Delete the test value
            self.delete(test_key)

            return {
                "status": "success",
                "message": "Redis is working correctly",
                "test_key": test_key,
                "test_value": test_value,
                "retrieved_value": retrieved_value,
            }

        except Exception as e:
            logger.error(f"Redis test failed: {e}")
            return {"status": "error", "message": f"Redis test failed: {str(e)}"}

    def get_status(self) -> Dict[str, Any]:
        """Get Redis connection status."""
        return {
            "available": self.available,
            "host": self.host,
            "port": self.port,
        }


# Global Redis client instance
redis_client = RedisClient()
