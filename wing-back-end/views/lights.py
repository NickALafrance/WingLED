from controller.WebEvent import WebEvent

def light(event: WebEvent):
    if event.isRead():
        event.responseData.update({ 'strip': event.modelData.strip.position })
        event.responseData = event.modelData.serialize()
