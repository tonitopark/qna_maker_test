########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'your-service-key',
}

from urllib.parse import urlencode, quote_plus

body = """
{"name": "QnA Maker FAQ Tony",
  "qnaList": [
    {
      "id": 0,
      "answer": "You can change the default message if you use the QnAMakerDialog. See this for details: https://docs.botframework.com/en-us/azure-bot-service/templates/qnamaker/#navtitle",
      "source": "Custom Editorial",
      "questions": [
        "How can I change the default message from QnA Maker?"
      ],
      "metadata": []
    },
    {
      "id": 0,
      "answer": "You can use our REST apis to manage your KB. See here for details: https://westus.dev.cognitive.microsoft.com/docs/services/58994a073d9e04097c7ba6fe/operations/58994a073d9e041ad42d9baa",
      "source": "Custom Editorial",
      "questions": [
        "How do I programmatically update my KB?"
      ],
      "metadata": [
        {
          "name": "category",
          "value": "api"
        }
      ]
    }
  ],
  "urls": [
    "https://docs.microsoft.com/en-in/azure/cognitive-services/qnamaker/faqs",
    "https://docs.microsoft.com/en-us/bot-framework/resources-bot-framework-faq"
  ],
  "files": [
    {
      "fileName": "SurfaceManual.pdf",
      "fileUri": "https://download.microsoft.com/download/2/9/B/29B20383-302C-4517-A006-B0186F04BE28/surface-pro-4-user-guide-EN.pdf"
    }
  ]
}
"""
#params = urllib.parse.urlencode(payload, quote_via=quote_plus)
#

try:
    conn = http.client.HTTPSConnection('your-host')
    conn.request("POST", "/qnamaker/v4.0/knowledgebases/create",body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

########