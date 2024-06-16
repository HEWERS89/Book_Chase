
# User Stories for Book Reviews

As a registered user, I want to be able to write and publish a book review so that I can share my thoughts and opinions about a book with others.
Acceptance Criteria:
The user is logged in to their account.
The user can enter a book title, edit and review their own reviews.
The user can submit the review for publication.
The review is published on the website and associated with the user's account name.

As a registered user, I want to be able to edit and update my previously published book reviews so that I can correct errors or add new insights.
Acceptance Criteria:
The user is logged in to their account.
The user can access their previously published book reviews.
The user can edit the review text, or other details.
The updated review is saved and published on the website.

As a registered user, I want to be able to view book reviews from other users so that I can discover new books and get different perspectives.
Acceptance Criteria:
The user is logged in to their account.
The user can search for book reviews by title, author, or ISBN.
The user can view a list of book reviews from other users.
Each review includes the user's username and their associated review.

## Features:
User functionality: Functionality for users to create, locate, display, edit and delete records.

## Design:

## Colour scheme:

## Deployment
The site was deployed to GitHub.

Follow the steps to deploy:

In the Github repository, open the settings tab
From the drop-down menu, select Main branch and then Save

## Local Deployment

To make a local copy of this project, you can clone it. In your IDE, type the following command:
git clone https://hewers89.github.io/Book_Chase/

## Testing

### Light House

- Login Page [Desktop]
  [Mobile]
- Home Page [Desktop]
  [Mobile]
- Add Book Page [Desktop]
  [Mobile]
- Search Page [Desktop]
  [Mobile]
- Profile Page [Desktop]
  [Mobile]


### Chrome Responsive Viewer

- Login Page [Desktop]
  [Mobile]
- Home Page [Desktop]
  [Mobile]
- Add Book Page [Desktop]
  [Mobile]
- Search Page [Desktop]
  [Mobile]
- Profile Page [Desktop]
  [Mobile]

### Manual Testing

# **Testing**


|             | User Action | Expected result  | Y/N | Comment |
|-------------|-------------|------------------|-----|---------|
|Sign Up      |             |                  |     |         |
|           | Click LOGIN button in home page | Login page | Y | Login page opens 
|            | Click on REGISTER from link on login page| Register Page | Y | Register page opens |
|           | Enter valid username and password | Profile page opens | Y | User is signed up |
| Log In      |             |                  |     |         |
|            | Click on Login button in home page | Login page | Y | Login page opens |
|           | Enter valid username and password | Profile page | Y | User is redirected to their profile page if registerd user if not flash message displays to register |
|Log Out      |             |                  |     |         |
|            | Click on logout button which displays automaticaly where the login button was once logged in | Home page | Y | User is logged out displaying flash message as confirmation |
|            | Click browser back button | You are still logged out | Y | Session is ended |
|Search   |             |                  |     |         |
|            | Click searchk button | Search page| Y | Search page opens |
|            | CLick radio buttons for search options | Visual display of radio buttons in use | Y | Search using radio buttons for the specific option or error message displays |
|            | Click search button | Display of search results or error messgae of 'no books found' | Y | Search results display or error message |
|Result links  |             |                  |     |         |
|            | Click tilte of book| Display of book details and reviews by users| Y | Book details and reviews display with option to leave a review |
|            | Click submit review button | Submits review | Y | Submits review and instantly displays or if already submitted review doesnt allow the user to submit with flash message |
|Add Book  |             |                  |     |         |
|            | Click add book button | Opens add book page | Y | Displays add book page |
|            | Click add book button | Adds book details to collection | Y | Confirmation flash message  |
|Profile Page |             |                  |     |         |
|            | Click profile button |Profile button redirects to profile | Y | Profile button displays after log in and disapears after log out |
|            | My reviews and My books | Users reviews and books added display | Y | Shown on the users profile page  |
|            | Click edit/delete button | Removes or updates the book/review | Y | Confirmation flash message of update or delete |
|Footer Links  |             |                  |     |         |
|            | Click  | clickable no link | Y | Asthetic purpose only|
|Home Page |             |                  |     |         |
|            | Click links | clickable no link | Y | Asthetic purpose only|

### Compatibility

[Google Chrome](https;//google.co.uk) Manually tested on google chrome for functionality , appearance  and responsiveness. All features passed.

[Internet Explorer](https://www.microsoft.com/en-gb/download/internet-explorer.aspx) Manually tested on google chrome for functionality , apperance and responsiveness. All features passed.

### Validator

[Javascript]()

[HTML]()

[CSS]()

## Bugs

The answers were duplicating instead of moving to the next question, this was due to a +1 i added to questions in javascript once removed this stopped the duplication.

The reset button didn't reset the question counting, I passed the value of 0 to reset the counter at the click of reset. 


## Languages

[HTML](https://www.w3schools.com/html/) for the foundation of the site.

[CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) used to add style and layout.

[JavaScript](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/First_steps/What_is_JavaScript) used to add functionality to the game

[Flexbox](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Flexbox) to arrange items and make them responsive.

[VScode](https://code.visualstudio.com/) used as my tool for writing and editing code.

[Github](https://github.com/) used to host the code of the website.

[Gitpod](https://www.gitpod.io/) an open source CDE

[Python] 

[Flask]



## Hero Image
#### Background image used available via this [link](https://www.pexels.com/photo/books-in-black-wooden-book-shelf-159711/)


# Data Schema

## Users Collection

_id (ObjectId): unique identifier for each user
username : username chosen by the user
password: hashed password for the user
books (array of ObjectId): list of book IDs added by the user

## Books Collection

_id (ObjectId): unique identifier for each book
title (string): title of the book
author (string): author of the book
isbn (string): ISBN number of the book
added_by (string): username of the user who added the book

## Reviews Collection

_id (ObjectId): unique identifier for each review
book_id (ObjectId): ID of the book being reviewed
username (string): username of the user who wrote the review
comment (string): text of the review

## The relationships between the collections are as follows:

A user can add multiple books (one-to-many).
A book can have multiple reviews (one-to-many).
A review is associated with one book and one user (many-to-one).

