from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import time
import json

# For certificate based connection
myShadowClient = AWSIoTMQTTShadowClient("my-iot-thing")
# It can be same as the Thing’s name “my-iot-thing” we created above
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
# Configurations
# For TLS mutual authentication
ENDPOINT = "a32glxhe0xutf2-ats.iot.us-east-1.amazonaws.com"
#myShadowClient.configureEndpoint("ENDPOINT", 8883)
# The Endpoint can be found in the Interact part in the details of your Thing which showed above
# For Websocket
myShadowClient.configureEndpoint(ENDPOINT, 443)
# For TLS mutual authentication with TLS ALPN extension
# myShadowClient.configureEndpoint("YOUR.ENDPOINT", 443)
myShadowClient.configureCredentials("/home/a/mu_code/iot-thing/AmazonRootCA1.pem",
"/home/a/mu_code/iot-thing/433bc6f2db344cdf4e911e796a9930fa7b36b620b2ebccbf7a18a623b58bc885-private.pem.key",
"/home/a/mu_code/iot-thing/433bc6f2db344cdf4e911e796a9930fa7b36b620b2ebccbf7a18a623b58bc885-certificate.pem.crt")
# The three files which we transferred earlier, get the path easily using the method above
# For Websocket, we only need to configure the root CA
# myShadowClient.configureCredentials("YOUR/ROOT/CA/PATH")
myShadowClient.configureConnectDisconnectTimeout(10) # 10 sec
myShadowClient.configureMQTTOperationTimeout(20) # 5 sec
def customShadowCallback_Update(payload, responseStatus, token):
 # payload is a JSON string ready to be parsed using json.loads(...)
 # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + "accepted!")
        print("property: " +
        str(payloadDict["state"]["reported"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")


def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + "accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!")


myShadowClient.connect()
# Create a device shadow instance using persistent subscription
myDeviceShadow = myShadowClient.createShadowHandlerWithName("my-iot-thing", True)
# The Thing Name is what we created initially, it should be “my-iot-thing” in the case above
# Delete shadow JSON doc
myDeviceShadow.shadowDelete(customShadowCallback_Delete, 5)
# Shadow operations
# This is the shadow message we want to update to the AWS
# NOTE: Don’t put these comment lines into the JSON area
# otherwise it will be wrong and update nothing
JSONPayload = """{ "state":
 { "reported":
 { "time":"12:00",
 "temperature":"50"
 }
 },
"message": "Hello from AWS IoT console"
}"""
# Update shadow JSON
myDeviceShadow.shadowUpdate(JSONPayload,customShadowCallback_Update, 5)