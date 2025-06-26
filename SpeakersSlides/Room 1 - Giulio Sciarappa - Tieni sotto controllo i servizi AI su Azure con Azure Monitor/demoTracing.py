#prima di tutto ricorda di export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true su terminale!!!!!
import os
from openai import AzureOpenAI
#QUESTI
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

OpenAIInstrumentor().instrument()
#inserisci il nome dell'endpoint corretto
endpoint = "https://ilnomedelaifoundry.cognitiveservices.azure.com/"
model_name = "gpt-4o"
deployment = "gpt-4o"
#decommentare la riga sottostante e inserire la chiave di sottoscrizione 
#subscription_key = "LASUBSCRIPTIONKEYNELFORMATOALFANUMERICO"
api_version = "2024-12-01-preview"
#nella normalità automatizzo l'ottenimento della connection string ma per il demo la metto fissa, nel caso inseriscila al posto della riga sottostante
#connection_string = "InstrumentationKey=instrumentationkey;IngestionEndpoint=https://swedencentral-0.in.applicationinsights.azure.com/;LiveEndpoint=https://swedencentral.livediagnostics.monitor.azure.com/;ApplicationId=idAppinsight"

#questo permette di configurare il monitoraggio di Azure
configure_azure_monitor(connection_string=connection_string)
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)
#abilito il tracer
tracer = trace.get_tracer(__name__)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "I am going to Rome, what should I see? consider that Tivoli is not Rome",
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=deployment
)

print(response.choices[0].message.content)