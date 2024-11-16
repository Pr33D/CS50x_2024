# CS50x Final Project

## Taskz
Task Manager Web-Application with day and calender overview
Languages: Python/Flask, Javascript, HTML, SCSS -> CSS, SQL

  ### Demonstration video
  Lets have a look at the program itself in live action:
  
  [![Screenshot of the web page](https://img.youtube.com/vi/8uGSIDwcTro/default.jpg)]([www.google.com](https://www.youtube.com/watch?v=8uGSIDwcTro))

  ### App Description
  Taskz is a simple, little task manager with 3 different overview pages including a complete, a calender and a single day overview to stay focussed at your needs.

  ### Basic functionality
  - Create an own User Account to have your tasks saved in the database - especially for you!
  - Session driven to keep you logged in while offline
  - Manage taskz (Yeah, spelled with a "z") on the Overview page, where all your taskz are listed, ordered by date descending
    - Check off or uncheck taskz. Checked off tasks are grayed out and stored in a lower section to not interrupting your workflow. There, you can see the date of creation to simple remember, when you added the task. They stay in standby, so you can reactivate them, if needed
    - Delete taskz, if not needed anymore (by deletion, it will be gone forever! No possibility to restore!)
  - Add tasks using a simple web form with due date, or even without to have the task always at the Top
    - After creating a task it will automatically generate quick access links to the calendar month and another for the day its supposed to be done
  - Choose from light or dark mode

  ### Working with calender
  - directly jump into the day of the task, where you can see other tasks on that specific date
  - Monthly calender with up/down functionality, showing tasks of the month underneath it
  - Calendar and day can be reaccessed by simply copy and paste the URL, which has the month, day and year information in it

  ### Design
  The Design of the Web App is, compared to other websites, upside down - Why? Ever tried to access the navigation bar on your 6 inch+ Smartphone or Tablet without using your second hand? Thats why.
  The navigation bar is also changeable. While it contains a Link to the contact page and impressum for everyone, it only contains links to the overview and create task pages when logged in because of simplicity.
  Avoiding overload, its much easier to find, what youre looking for.
  The "Taskz"-Logo will bring you either to the index page with a little picture, or to the overview page of your taskz depending on your session state.

  ### Other
  - Contact form gives you direct, javascript controlled, feedback. Its not sending any email to anyone
  - There are different flash messages built in.
    - Registration failed? You get a message showing you everything went wrong
    - Login failed? Maybe the name was not right. Try it again. The flash message tells you what to do
    - Task added - You will see a message
    - and so on ...

#### Thank you