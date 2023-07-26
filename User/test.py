from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Profile
from .serializers import ProfileSerializer


class ProfileAPITestCase(APITestCase):
    def setUp(self):
        # 在測試資料庫中創建一個測試用的 UserProfile
        self.test_uid = 'test_uid_123'
        self.profile_data = {
            "email": "test@example.com",
            "username": "testuser",
            "phone": "1234567890",
            # 添加其他需要的資料
        }
        self.profile = Profile.objects.using("user").create(
            id=self.test_uid, **self.profile_data)

    def test_profile_update(self):
        url = reverse('profile', args=[self.test_uid])  # 替換成您的實際 URL，並提供 uid
        updated_data = {
            "email": "updated_test@example.com",
            "phone": "9876543210",
            # 添加其他需要更新的資料
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 確認資料是否更新成功
        updated_profile = Profile.objects.using("user").get(id=self.test_uid)
        serializer = ProfileSerializer(updated_profile)
        self.assertEqual(serializer.data["email"], "updated_test@example.com")
        self.assertEqual(serializer.data["phone"], "9876543210")
        # 確保其他需要更新的欄位也已經更新成功
