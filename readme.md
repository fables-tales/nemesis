#Nemesis

This is Nemesis, a new system for allowing team leaders running teams for the
[Student Robotics](http://studentrobotics.org) competition to change their passwords.

##Phippen, you ass, just let me hack on it

Ok cool, run this (anywhere that isn't in a git repository), also this command
downloads a ~400 meg ubuntu vm image.

```shell
curl https://raw.github.com/samphippen/nemesis/master/setup.sh | bash && cd srobo-ldap-box
```

After that, follow the final setup instructions (they get printed to the screen).
Once you're all run, the server can be started by starting the venv, and starting
the server. The vm forwards port 5000 to localhost:5000, so you do this

```shell
source venv/bin/activate
cd nemesis
python app.py
```

and then point your browser at localhost:5000. This allows you to do testing.

Teachers are:
<table>
    <tr>
        <th>Username</th><th>Password</th>
    </tr>
    <tr>
        <td>teacher_coll1</td><td>facebees</td>
    </tr>
        <td>teacher_coll2</td><td>noway</td>
    </tr>
</table>



##Setting it up the difficult way™

Your LDAP needs to be configured like [this](https://www.studentrobotics.org/trac/wiki/PrepareLDAP).
If you're putting this into development and want to run the test suite you'll need
users exactly as the box expects.

The easiest way to do this is install userman after you've configured the box
and then run these userman commands (your LDAP **must** be empty for this to work):

```shell
./userman user add teacher_coll1 teacher teacher teacher@teacher.com
./userman user add teacher_coll2 teacher2 teacher teacher2@teacher.com

./userman user add student_coll1_1 student1 student student1@teacher.com
./userman user add student_coll1_2 student2 student student2@teacher.com

./userman user add student_coll2_1 student3 student student3@teacher.com
./userman user add student_coll2_2 student4 student student4@teacher.com

./userman college create "college the first"
./userman college create "secondary college"

./userman group create teachers
./userman group create students student

./userman group create team1
./userman group create team2
./userman group create team3

./userman group addusers teachers teacher_coll1
./userman group addusers teachers teacher_coll2

./userman group addusers students student_coll1_1
./userman group addusers students student_coll1_2
./userman group addusers students student_coll2_1
./userman group addusers students student_coll2_2

./userman group addusers college-1 teacher_coll1
./userman group addusers college-1 student_coll1_1 student_coll1_2

./userman group addusers college-2 teacher_coll2
./userman group addusers college-2 student_coll2_1 student_coll2_2

./userman group addusers team1 teacher_coll1 student_coll1_1
./userman group addusers team2 teacher_coll1 student_coll1_1


./userman group addusers team3 teacher_coll2 student_coll2_1 student_coll2_2

#set the user's password to 'facebees'
echo "type 'facebees'"
./userman user passwd teacher_coll1

#set the user's password to 'noway'
echo "type 'noway'"
./userman user passwd teacher_coll2

#set the user's password to 'cows'
echo "type 'cows'"
./userman user passwd student_coll1_1
```

###In production:
In `nemesis/userman/sr/config.ini` all the ports, username and passwords need
to be set, and the user needs to have like the right permissions, which is
some subset of the things userman needs, plus change email.
