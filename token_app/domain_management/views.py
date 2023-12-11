# Finalement pas utilisé

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Subdomain
from .serializers import SubdomainSerializer
from rest_framework import status
from rest_framework.exceptions import NotFound
import requests

# URL de base et clé API pour PowerDNS
POWERDNS_API_URL = 'http://127.0.0.1:8081'
POWERDNS_API_KEY = 'Sup3rAp1K3yDuTurfu'
DOMAIN = 'turbo-upload.com.'

class SubdomainListView(APIView):
    def get(self, request, format=None):
        subdomains = Subdomain.objects.all()
        serializer = SubdomainSerializer(subdomains, many=True)
        return Response(serializer.data)

class SubdomainCreateView(APIView):
    def post(self, request, format=None):
        serializer = SubdomainSerializer(data=request.data)
        if serializer.is_valid():
            # Créer le sous-domaine dans Django
            subdomain = serializer.save()
            
            # Préparation de la requête pour PowerDNS
            dns_data = {
                "rrsets": [
                    {
                        "name": f"{subdomain.name}.{DOMAIN}",
                        "type": "A",
                        "ttl": 3600,
                        "changetype": "REPLACE",
                        "records": [
                            {
                                "content": "217.182.204.112",
                                "disabled": False
                            }
                        ]
                    }
                ]
            }
            
            # Créer l'enregistrement DNS dans PowerDNS
            response = requests.patch(
                f"{POWERDNS_API_URL}/zones/{DOMAIN}",
                headers={'X-API-Key': POWERDNS_API_KEY},
                json=dns_data
            )
            if response.status_code == 201:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Gérer l'erreur avec PowerDNS ici
                subdomain.delete()  # Supprimer le sous-domaine en cas d'erreur
                return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubdomainDeleteView(APIView):
    def delete(self, request, pk, format=None):
        try:
            subdomain = Subdomain.objects.get(pk=pk)

            # Préparation de la requête pour supprimer le sous-domaine dans PowerDNS
            dns_data = {
                "rrsets": [
                    {
                        "name": f"{subdomain.name}.{DOMAIN}",
                        "type": "A",
                        "changetype": "DELETE",
                    }
                ]
            }

            # Supprimer l'enregistrement DNS dans PowerDNS
            response = requests.patch(
                f"{POWERDNS_API_URL}/zones/{DOMAIN}",
                headers={'X-API-Key': POWERDNS_API_KEY},
                json=dns_data
            )
            if response.status_code in [200, 204]:
                subdomain.delete()  # Supprimer le sous-domaine dans Django
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                # Gérer l'erreur avec PowerDNS ici
                return Response(response.json(), status=response.status_code)
        except Subdomain.DoesNotExist:
            raise NotFound("Le sous-domaine spécifié n'a pas été trouvé.")
