# Mobile Legends Draft Pick Simulator

#### Video Demo:  https://youtu.be/WSQidGXNb8M

## Overview

The **Mobile Legends Draft Pick Simulator** is a web-based tool designed to emulate the ranked draft pick system in the popular game, **Mobile Legends: Bang Bang**. This project provides users with an interactive interface to pick, ban, and swap heroes during the drafting phase, mimicking the experience of strategizing in ranked matches. It supports user authentication, enabling personalized sessions where users can save and resume their drafts.

This project is built using Python and Flask for the backend, along with Bootstrap for a responsive and clean front-end design.

## Features

1. **Hero Selection and Management**:
   - Users can pick, ban, and swap heroes dynamically within the interface.
   - Heroes that have already been selected (picked, banned, or swapped) become unavailable to ensure authenticity.
   - Interactive slots, users can click on any hero placed in a slot to remove them, making them available for selection again.

2. **User Authentication**:
   - Users can create an account, log in, and access their personalized drafts.
   - Guest users can still interact with the simulator but lack the ability to keep drafts for long and access them over multiple devices.

3. **Draft Management**:
   - Users can save drafts in progress to revisit them later.
   - The main page displays a list of saved drafts and an option to start fresh.

4. **API-Driven Hero Data**:
   - The application fetches API data from a [GitHub repository](https://github.com/p3hndrx/MLBB-API), which includes hero names, roles, and images. Credit goes to **p3hndrx** for providing this resource, ensuring an accurate and visually immersive experience.

## File Descriptions

### HTML Files

1. **`base.html`**
   Acts as the layout for other pages, reducing redundancy in HTML. Common components like the navigation bar and flash message are defined here.

2. **`draft.html`**
   This is the heart of the application. It allows users to simulate the drafting process, providing an interactive experience to pick and ban heroes. The logic ensures that:
   - Selected heroes are dynamically removed from the available pool.
   - Users can click on slots to clear selections, making heroes available again.

3. **`login.html`**
   A dedicated page for users to log into their accounts.

4. **`signup.html`**
   A page where new users can create accounts. It utilizes basic security features, such as password hashing, to protect user data.

5. **`main.html`**
   The landing page for users. This page displays a list of drafts saved by the user, enabling them to resume previous sessions. It also features a button to create a new draft from scratch.

### Backend

1. **`app.py`**
   The main Flask application that powers the backend. It includes:
   - Routes for user authentication (login, signup, logout).
   - Routes for managing drafts (save, view).

## Technologies Used

- **Backend**: Python with Flask
- **Frontend**: HTML5, CSS3, JavaScript, and Bootstrap
- **Database**: SQLite for storing user data and saved drafts
- **API Integration**: Hero data from the [MLBB-API GitHub repository](https://github.com/p3hndrx/MLBB-API) by **p3hndrx**

## How to Use

1. **Setup**:
   - Clone the repository.
   - Set up a Python virtual environment and install the required dependencies using `pip install -r requirements.txt`.
   - Run the Flask application locally using `flask run`.

2. **Interact with the Simulator**:
   - Access the application through `localhost:5000`.
   - Sign up or log in to save your drafts, or use it as a guest for quick access.

3. **Draft Simulation**:
   - Click heroes from the list to assign them to pick or ban slots.
   - Remove heroes from slots by clicking on them, making them available again.
   - Save your draft at any time to resume later.

4. **Custom Hero Data**:
   - Modify the hero API data in `app.py` to reflect changes in the Mobile Legends roster or to customize the hero pool.

## Future Improvements

- Add support for custom game modes and team compositions.
- Include a timer to mimic the countdown during draft phases.
- Enhance the user interface with animations and improved accessibility.
- Implement a tutorial for first-time users.
