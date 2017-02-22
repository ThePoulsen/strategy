from app.crud.userCRUD import getUsers

def usersTable():
    users = getUsers(includes=['includeRoles', 'includeGroups'])['users']

    tableData = []
    for u in users:
        roles = ''
        for r in u['roles']:
            roles = roles + str(r['title']) +'<br>'
        groups = ''
        for gr in u['groups']:
            groups = groups + str(gr['name']) +'<br>'
        temp = [u['uuid'],u['name'],u['email'], roles, groups]
        tableData.append(temp)

    return tableData
