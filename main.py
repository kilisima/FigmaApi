from datetime import datetime
import os
from dotenv import load_dotenv
import yaml
import json
from FigmaApi import FigmaApi
from dateutil import parser
import sqlite3
import traceback

# .envファイルの内容を読み込みます
load_dotenv()

TEAM_LIST_FILE="teams.yaml"
api = FigmaApi(os.environ['FIGMA_TOKEN'])

def loadTeams():
    with open(TEAM_LIST_FILE) as file:
        teams = yaml.safe_load(file.read())
        return teams 

def dropTable(con:sqlite3.Connection):
    sql = "DROP TABLE IF EXISTS figmadata;"
    con.execute(sql)
    pass

def createTable(con:sqlite3.Connection):
    sql = """CREATE TABLE IF NOT EXISTS figmadata (
        teamId INTEGER,
        projectId INTEGER,
        fileKey TEXT,
        userId INTEGER,
        handle TEXT,
        date DATETIME,
        count INTEGER,
        PRIMARY KEY(teamId, projectId, fileKey, userId)
    )
    """ 
    con.execute(sql)
    con.commit()
    pass

def insertData(con:sqlite3.Connection, teamId:int, projectId:int, fileKey:str,userId:int,handle:str, date:str, count:int):
    data = (teamId, projectId, fileKey, userId, handle , date , count)
    sql = "replace into figmadata values (?,?,?,?,?,?,?);"
    con.execute(sql , data)
    con.commit()
    pass


def dbConnect():
    DBFILE = "data.db"
    return sqlite3.connect(database=DBFILE)

def dbClose(con:sqlite3.Connection):
    con.close()
    pass
    
    

def main():
    
    # os.environを用いて環境変数を表示させます
    print (os.environ['FIGMA_TOKEN'])
    teams = loadTeams()
    print(teams)

    # Debug用、自分の情報を取得
    myInfo = api.getMyUser()
    print(myInfo)

    
    summaryData = {}
    for teamId in teams["team_id"]:
        
        # チーム情報から、プロジェクト一覧を取得
        projects = api.getProjectsByTeamId(teamId)
        print(projects)

        for projectInfo in projects["projects"]:
            # projectIds.append(projectInfo["id"])
            projectId = projectInfo["id"]

            filesInfo = api.getFilesInfo(projectId)
            print(filesInfo)
            


            for fileInfo in filesInfo["files"]:
                fileKey = fileInfo["key"]



                print(fileKey)
                history = api.getFileHistory(fileKey)
                print(json.dumps(history, indent=2))


                for version in history["versions"]:
                    handle = version["user"]["handle"]
                    uid = version["user"]["id"]
                    createdAt = parser.isoparse(version["created_at"])
                    date = createdAt.strftime("%Y-%m-%d")

                    summaryKey = f"{teamId}-{projectId}-{uid}-{date}"
                    if summaryKey not in summaryData:
                        summaryData[summaryKey] = {}
                        summaryData[summaryKey]["count"] = 0
                        summaryData[summaryKey]["teamId"] = int(teamId)
                        summaryData[summaryKey]["projectId"] = int(projectId)
                        summaryData[summaryKey]["fileKey"] = fileKey
                        summaryData[summaryKey]["uid"] = int(uid)
                        summaryData[summaryKey]["date"] = date
                        summaryData[summaryKey]["handle"] = handle

                    summaryData[summaryKey]["count"] += 1
                    


    print("summaryData", summaryData)
    con = dbConnect()
    dropTable(con)
    createTable(con)
    for value in summaryData:
        print(value)
        data = summaryData[value]
        insertData(con, data["teamId"], data["projectId"], data["fileKey"], data["uid"], data["handle"], data["date"], data["count"])
    
    dbClose(con)
    pass




if __name__ == "__main__":
    try:

        main()
    except Exception as e:
        print(traceback.format_exc())

    
    pass