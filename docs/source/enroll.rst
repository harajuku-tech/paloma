================
Enrollment
================

Web Sign Up
==================

- Standart Sign Up flow

Flow
-----

- User visit the site
- Goto Sign Up Page
- Fill the Sign Up Form

    - login name
    - password
    - email
    - selected Groups

- Create User and Mailbox model 

    - update Mailbox.secret with new unique secret 
    - update Mailbox.dt_secret with now()

- send Sign Up greeting mail with sign up confirmation url.

    - update Maiibox.dt_sent
    - send email to Mailbox.address

- User visits to confirmation url

    - find Mailbox by  secret in confirmatil url.
    - check expirey
    - enable User and Mailbox 
    - set authentication cookie to UA. (or redirect to login page)

Mail Sign Up
==================

Flow
-----

- User visite the site
- Select Groups   
- Mailbox provide and Sign Up Try email is provided to the Page
- User click the link
- Send email without subject and body.
- Bounce handler looks for Mailbox with Group name and secrete in "to address".
- If mailbox fine, paloma crete Django User with random user name and password.

    - email is copy of "From mail" 

- Return greeting mail 
- User visits to confirmation url

    - same as web sign up.

Mail Sign In
==================

- Basicall, "Do your forget your password? "

Flow
-----

- User send mail to Sing In address (group-in@domain )
- Paloma bounce handler finds Mailbox for Group and "From address".
- Update Mailbox 
- Paloma returns greeting mail with confirmation url.
- User vistes to confirmatil url

    - same as web sign up

Invitation
==============

.. todo::
    - Invitation flow...

Irregular Case
======================

Existing Users try Mail Sign Up
---------------------------------------

If an exiting Mailbox founds, Paloma do the followings:

- Adds the spcified Group to the found Mailbox.
- Drop the new Mailbox for the Secret with no "address".
- Change to the Mail Sign In flow.  

Expired new Mailbox?
------------------------------

- To be deleted periodicall .
