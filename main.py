import datetime
from flask import Flask
from data.db_session import global_init, create_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_name = "db/blogs.db"
global_init(db_name)
db_sess = create_session()
# job = Jobs()
# job.collaborators = "2, 3"
# job.team_leader = 1
# job.work_size = 15
# job.is_finished = False
# job.start_date = datetime.datetime.now()
# job.job = "Something doing worker"
# print(1)
# db_sess.add(job)
# db_sess.commit()


@app.route("/")
def index():
    page_to_load = """<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet" 
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                    crossorigin="anonymous">
                    <title>Привет, Яндекс!</title>
                  </head>
                  <body>
                  <h1 align="center">Works log</h1>"""
    for i in db_sess.query(Jobs):
        page_to_load += f"""\n<table class="table caption-top">
      <caption>Action #{i.id}</caption>"""
        user_ = db_sess.query(User).filter(i.team_leader == User.id).first()
        surname_name = f"{user_.surname} {user_.name}"
        page_to_load += f"""<thead>
                <tr class="table-secondary">
                  <th scope="col">Title of activity</th>
                  <th scope="col">Team leader</th>
                  <th scope="col">Duration</th>
                  <th scope="col">List of collaborations</th>
                  <th scope="col">Is finished</th>
                </tr>
              </thead>
              <tbody>
                <tr class="table-primary">
                  <td>{i.job}</td>
                  <td>{surname_name}</td>
                  <td>{i.work_size} hours</td>
                  <td>{i.collaborators}</td>
                  {"<td>Finished" if i.is_finished 
                  else "<td class='table-danger'>Is not finished"}</td>
                </tr>
              </tbody>
            </table>"""
    page_to_load += "</body>\n</html>"
    return page_to_load


app.run(port=8080, host='127.0.0.1')
