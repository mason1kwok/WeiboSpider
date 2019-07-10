import constants
import models
import face
import click

@click.group()
def cli():
    pass

@cli.command("find")
@click.option("-u", "--url")
@click.option("-t", "--threshold", default=0.4)
def find(url, threshold):
    faces = face.url2faces(url)
    for encodings in faces:
        if len(encodings) > 0:
            vid = models.find_vid(encodings, threshold)
            if vid is None:
                continue
            imgs = models.find_image(vid)
            if imgs.count() <= 0:
                continue
            for img in imgs:
                click.secho(img.get('url'), bold=True, fg='green')
                for f in img.get("relations"):
                    for data in models.find_sina(f["from"], f["from_id"]):
                        click.secho("  FORM: %s ID: %s" % (f["from"], f["from_id"]), bold=True)
                        for k, v in data.items():
                            click.secho("    %s: %s" % (k, v))

            
            

if __name__ == '__main__':
    cli()
    if constants.connection_db is not None:
        constants.connection_db.close()