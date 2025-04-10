# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from jobspy import scrape_jobs
import numpy as np

class DataView(APIView):
    def get(self, request):
        try:
            jobs = scrape_jobs(
                site_name=["indeed", "linkedin", "glassdoor", "google"],
                # search_term="software",
                # google_search_term="software jobs",
                # location="San Francisco, CA",
                location=None,
                results_wanted=10000,
                hours_old=168,
                # country_indeed='USA',
            )

            # Replace NaN with None to make it JSON serializable
            jobs = jobs.replace({np.nan: None})

            # Convert to list of dicts (for JSON response)
            jobs_json = jobs.to_dict(orient="records")

            return Response({
                "message": f"Found {len(jobs_json)} jobs",
                "jobs": jobs_json
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)