# docker-xeoma

This is a docker container that runs a webserver that is used to publish MQTT messages. This is so Xeoma's HTTP Request Sender module can be used to send MQTT events that can later be intercepted by something like [Home Assistant](https://home-assistant.io/). The idea in the future is to add support for MQTT messages coming back to Xeoma via the HTTP Switch module in the future. Pull Requests are welcome!

This docker image is available [on Docker Hub](https://hub.docker.com/r/skylord123/xeoma-mqtt).

## Running

To launch the container:

`docker run -d --name=Xeoma -p 5000:5000 -v /local/path/to/config:/config skylord123/xeoma-mqtt`

When run for the first time, a file named config.ini will be created in the config dir, and the container will exit. Edit this file, and once complete, change `configured` to `True` and start (or restart) the container.

View logs using:

`docker logs xeoma-mqtt`

## Usage

This container runs a python web server that listens on port `5000` by default. You can test that messages are being posted by using this URL:
`http://127.0.0.1:5000/xeoma_data_handle/<channel>/<msg>`
example:
`http://127.0.0.1:5000/xeoma_data_handle/frontyard_camera/1`

To send an MQTT message from Xeoma when motion is detected just add a HTTP Request Sender module chained after the Motion module. Set the "Host name or IP Address" to `<host>/xeoma_data_handle/<channel>/<msg>` and "Port" to `5000` and make sure that the "Send" dropdown has "when event started" selected. You can optionally set the "Sending interval" (you will have to test what works best for you).

If you want to detect when the event ended as well you will have to create the same module side-by-side but change the `<msg>` in the path as well as the "Send" dropdown to "when event ended".

## Issues

There is currently an issue with the authentication. Just leave blank for now.

### Support

If you find any bugs with the software that are related to the docker container, let me know on GitHub with and Issue. If you find bugs that are related to the actual software or cameras, etc then contact FelenaSoft.

## Credits

Thanks to [Coppit](https://github.com/coppit) for creating an awesome [Xeoma container](https://github.com/coppit/docker-xeoma) (and for giving me a readme I could base mine off)
