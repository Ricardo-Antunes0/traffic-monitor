from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import RoadSegment, SpeedReading

"""
Testes unitários realizados: 
- Modelos (RoadSegment, SpeedReading): criação, campos obrigatórios, cálculo de intensidade, relações FK.
- Permissões da API: acesso de utilizadores anónimos e administradores.
- Endpoints da API: listagem, detalhes, contagem de leituras, última leitura e filtros por intensidade.
"""

class RoadSegmentModelTest(TestCase):
    """
    Testes para o modelo RoadSegment.
    
    Testa:
    - Criação de segmentos
    - Campos obrigatórios
    - Representação em string (__str__)
    """
    
    def setUp(self):
        """
        Executado antes de cada teste.
        Cria objetos necessários para os testes.
        """
        self.segment = RoadSegment.objects.create(
            longitude_start=10,
            latitude_start=30,
            longitude_end=10,
            latitude_end=30,
            length=30.29
        )
    
    def test_segment_creation(self):
        """
        Testa se um segmento é criado corretamente.
        """
        self.assertIsNotNone(self.segment.id)
        self.assertEqual(self.segment.longitude_start, 10)
        self.assertEqual(self.segment.length, 30.29)
    
    def test_segment_str(self):
        """
        Testa a representação em string do segmento.
        """
        expected = f"Segmento {self.segment.id}"
        print(self.segment)
        self.assertEqual(str(self.segment), expected) 


class SpeedReadingModelTest(TestCase):
    """
    Testes para o modelo SpeedReading.
    
    Testa:
    - Criação de leituras de velocidade
    - Cálculo de intensidade (elevada, média, baixa)
    - Relação com RoadSegment (FK)
    """
    
    def setUp(self):
        """
        Começar por criar um segmento para associar às leituras.
        """
        self.segment = RoadSegment.objects.create(
            longitude_start=10,
            latitude_start=30,
            longitude_end=10,
            latitude_end=30,
            length=30.29
        )
    
    def test_intensity_elevada(self):
        """
        Testa se a velocidade menor ou igual a 20 km/h resulta em intensidade elevada.
        """
        reading = SpeedReading.objects.create(
            road_segment=self.segment,
            average_speed=15.0,
            timestamp=timezone.now()
        )
        self.assertEqual(reading.intensity, 'elevada')
    
    def test_intensity_media(self):
        """
        Testa se a velocidade entre 20 e 50 km/h resulta em intensidade média.
        """
        reading = SpeedReading.objects.create(
            road_segment=self.segment,
            average_speed=35.44,
            timestamp=timezone.now()
        )
        self.assertEqual(reading.intensity, 'média')
    
    def test_intensity_baixa(self):
        """
        Testa se a velocidade maior que 50 km/h resulta em intensidade baixa.
        """
        reading = SpeedReading.objects.create(
            road_segment=self.segment,
            average_speed=100.0,
            timestamp=timezone.now()
        )
        self.assertEqual(reading.intensity, 'baixa')
    
    def test_reading_relationship(self):
        """
        Testa a relação FK entre SpeedReading e RoadSegment.
        """
        reading = SpeedReading.objects.create(
            road_segment=self.segment,
            average_speed=30.0,
            timestamp=timezone.now()
        )
        print(f"{reading}")
        print(f"{reading.road_segment} associado à {reading}")
        # Verificar se a leitura está associada ao segmento criado inicialmene
        self.assertEqual(reading.road_segment, self.segment)
        # Verificar se o segmento tem a leitura de velocidade associada a ele
        self.assertIn(reading, self.segment.readings.all())

class PermissionsTest(TestCase):
    """
    Testes para verificar as permissões da API.
    
    Testa:
    - Utilizador anónimo: pode fazer exclusivamente leituras (GET)
    - Utilizador administrador: pode fazer todo o tipo de operações
    """
    
    def setUp(self):
        """
        Cria:
        - Um admin com token
        - Um segmento de teste
        - Cliente da API
        """
        # Criar o admin
        self.admin = User.objects.create_user(
            username='admin',
            password='admin',
            is_staff=True
        )
        
        # Cria um token para o admin
        self.token = Token.objects.create(user=self.admin)
        
        # Cria segmento de teste
        self.segment = RoadSegment.objects.create(
            longitude_start=10,
            latitude_start=30,
            longitude_end=10,
            latitude_end=30,
            length=30.29
        )
        
        # Cliente da API (para simular pedidos HTTP à API)
        self.client = APIClient()
    
    def test_anonymous_can_get(self):
        """
        Testa se o utilizador anónimo consegue fazer um pedido GET.
        """
        response = self.client.get('/api/segments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_anonymous_cannot_post(self):
        """
        Testa se o utilizador anónimo não consegue fazer um pedido POST.
        """
        data = {
            'longitude_start': 10,
            'latitude_start': 30,
            'longitude_end': 10,
            'latitude_end': 30,
            'length': 510.5
        }
        response = self.client.post('/api/segments/', data)
        # Deve retornar 401 (Unauthorized) ou 403 (Forbidden)
        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED,
            #status.HTTP_403_FORBIDDEN
        ])
    
    def test_admin_can_post(self):
        """
        Testa se admin autenticado consegue fazer POST.
        """
        # Autentica com token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data = {
            'longitude_start': 10,
            'latitude_start': 30,
            'longitude_end': 10,
            'latitude_end': 30,
            'length': 510.5
        }
        response = self.client.post('/api/segments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_admin_can_delete(self):
        """
        Testa se o admin consegue apagar segmentos.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(f'/api/segments/{self.segment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class APIEndpointsTest(TestCase):
    """
    Testes para os endpoints da API.
    
    Testa:
    - Listar os segmentos
    - Detalhes de um segmento
    - Total de leituras no response
    - Última leitura no response
    - Filtro por intensidade
    """
    
    def setUp(self):
        """
        Criar segmentos e leituras para testar.
        """
        # Segmento com intensidade elevada
        self.segment_A = RoadSegment.objects.create(
            longitude_start=85.4,
            latitude_start=30.5,
            longitude_end=192.4,
            latitude_end=5.5,
            length=100.9
        )
        SpeedReading.objects.create(
            road_segment=self.segment_A,
            average_speed=15.0,
            timestamp=timezone.now()
        )
        
        # Segmento com intensidade média
        self.segment_B = RoadSegment.objects.create(
            longitude_start=104.0,
            latitude_start=31.0,
            longitude_end=104.1,
            latitude_end=31.1,
            length=10000.0
        )
        SpeedReading.objects.create(
            road_segment=self.segment_B,
            average_speed=35.0,
            timestamp=timezone.now()
        )
        
        # Segmento com intensidade baixa
        self.segment_C = RoadSegment.objects.create(
            longitude_start=105.0,
            latitude_start=32.0,
            longitude_end=105.1,
            latitude_end=32.1,
            length=9125.0
        )
        SpeedReading.objects.create(
            road_segment=self.segment_C,
            average_speed=65.0,  # baixa
            timestamp=timezone.now()
        )
        
        self.client = APIClient()
    
    def test_list_segments(self):
        """
        Testa se GET /api/segments/ retorna todos os segmentos.
        """
        response = self.client.get('/api/segments/')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_retrieve_segment(self):
        """
        Testa se GET /api/segments/{id}/ retorna os dados corretos.
        """
        response = self.client.get(f'/api/segments/{self.segment_A.id}/')
        print(f"Segmento A: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.segment_A.id)
        self.assertIn('total_readings', response.data)
        self.assertIn('latest_reading', response.data)
    
    def test_total_readings_in_response(self):
        """
        Testar se o campo total_readings está presente e correto.
        """
        response = self.client.get(f'/api/segments/{self.segment_A.id}/')
        print(f"\nSegmento A: {response.data}\n")
        self.assertEqual(response.data['total_readings'], 1)
        
        # Adiciona mais uma leitura ao segmento A
        SpeedReading.objects.create(
            road_segment=self.segment_A,
            average_speed=55.0,
            timestamp=timezone.now()
        )
        response = self.client.get(f'/api/segments/{self.segment_A.id}/')
        print(f"\n Segmento A com + 1 leitura: {response.data}\n")
        self.assertEqual(response.data['total_readings'], 2)
    
    def test_latest_reading_in_response(self):
        """
        Testa se a última leitura está presente no response.
        """
        # Adiciona mais uma leitura ao segmento A
        SpeedReading.objects.create(
            road_segment=self.segment_A,
            average_speed=55.0,
            timestamp=timezone.now()
        )

        response = self.client.get(f'/api/segments/{self.segment_A.id}/')
        print(f"\n Segmento A atualizado: {response.data}\n")
        self.assertIsNotNone(response.data['latest_reading'])
        self.assertEqual(response.data['latest_reading']['average_speed'],55.0)
        self.assertEqual(response.data['latest_reading']['intensity'],'baixa')
    
    def test_filter_by_intensity_elevada(self):
        """
        Testar filtrar por intensidade 'elevada'.
        """
        response = self.client.get('/api/segments/?intensity=elevada')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Apenas 1 com elevada
    
    def test_filter_by_intensity_media(self):
        """
        Testar filtrar por intensidade 'média'.
        """
        response = self.client.get('/api/segments/?intensity=média')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Apenas 1 com média
    
    def test_filter_by_intensity_baixa(self):
        """
        Testar filtrar por intensidade 'baixa'.
        """
        # Vou adicionar mais um segmento com intensidade baixa

        response = self.client.get('/api/segments/?intensity=baixa')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Apenas 1 com baixa
    
    def test_filter_readings_by_segment(self):
        """
        Testar o filtro de leituras por segmento.
        """
        response = self.client.get(f'/api/readings/?road_segment={self.segment_A.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Apenas 1 leitura deste segmento
