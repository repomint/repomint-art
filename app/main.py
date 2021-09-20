from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
import requests
headers = {'Accept': 'application/vnd.github.inertia-preview+json', 'Authorization':'token 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'}
app = Flask(__name__)

@app.route('/')
def background():
    if request.args.get('r'):
        r = int(request.args.get('r'))
    else:
        r=250
    if request.args.get('g'):
        g = int(request.args.get('g'))
    else:
        g=250
    if request.args.get('b'):
        b = int(request.args.get('b'))
    else:
        b=250

    first_im = Image.new(mode="RGBA", size=(300, 300), color = (r,g,b))

    if request.args.get('repo'):
        repo = request.args.get('repo')
        #get the name of the organization/team
        if repo[-1]=='/':
            team = repo.split('/')[-3]
        else:
            team = repo.split('/')[-2]
            repo = repo+'/'

        #get the team picture
        pic_team = requests.get(f'https://api.github.com/orgs/{team}', headers=headers)
        pic_team = pic_team.json()['avatar_url']
        pic_team = requests.get(pic_team).content

        #get the number of forks for the repo
        n_forks = requests.get(f'https://api.github.com/repos/{repo}forks', headers=headers)
        n_forks = len(n_forks.json())

        #get the number of contributors for the repo
        n_conts = requests.get(f'https://api.github.com/repos/{repo}contributors', headers=headers)
        n_conts = len(n_conts.json())

        #get the most significant language of the repo
        pr_lan = requests.get(f'https://api.github.com/repos/{repo}languages', headers=headers)
        pr_lan = next(iter(pr_lan.json()))

        #get the number of stargazers for the repo
        n_str = requests.get(f'https://api.github.com/repos/{repo}stargazers', headers=headers)
        n_str = len(n_str.json())

        #get the number of subscribers for the repo
        n_sub = requests.get(f'https://api.github.com/repos/{repo}subscribers', headers=headers)
        n_sub = len(n_sub.json())

        team_img = Image.open(BytesIO(pic_team)).convert("RGBA")
        team_img = team_img.resize((200, 200), resample=Image.NEAREST)
        first_im.paste(team_img,(50,0), team_img)

        draw = ImageDraw.Draw(first_im)
        draw.text((50, 210),f"{repo}",(0,0,0))
        draw.text((50, 225),f"Forks:{n_forks}",(0,0,0))
        draw.text((50, 240),f"Stars:{n_str}",(0,0,0))
        draw.text((50, 255),f"Contributors:{n_conts}",(0,0,0))
        draw.text((50, 270),f"Key language:{pr_lan}",(0,0,0))
        draw.text((50, 285),f"Subscribers:{n_sub}",(0,0,0))


    data = BytesIO()
    first_im.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template("index.html", img_data=encoded_img_data.decode('utf-8'))