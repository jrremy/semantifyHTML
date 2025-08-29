# SemantifyHTML

This project is a web tool that aims to enhance the semantic quality of HTML code to promote accessibility and improve SEO (Search Engine Optimization). Built using a React frontend and Flask backend, it allows users to paste HTML code, load it from a URL, or upload an HTML file, and get a more semantic version of the code along with explanations for each change.

## Features

- **HTML Code Enhancement**: Users can input HTML code, load it from a URL, or upload an HTML file to receive a more semantic version that enhances accessibility and SEO.

- **Explanations for Changes**: Provides AI-generated explanations via OpenAI's API for each modification made to the HTML code, helping users understand the improvements.

- **Accessibility-Driven Recommendations**: Ensures the generated HTML follows best practices for screen readers and other assistive technologies, making web pages more inclusive.

- **SEO Optimization**: Analyzes and adjusts HTML elements to improve discoverability by search engines.

## Motivation

I heavily value accessibility. I've seen firsthand how impactful tools like screen readers and magnifiers are, since I've used these tools myself. When I first learned about web development, I came across an interesting fact when exploring HTML: a lot of the tags you use may not make a visual difference on the page, but play a crucial role in the backend. These elements, &lt;header&gt;, &lt;article&gt;, and &lt;details&gt;, are referred to as semantic. They're responsible for letting the browser and search engine know what their purpose is, and can provide more details to something like a screen reader. Just simply adding an alternative description for an image can tell a visually impaired person what's on their screen. With this knowledge, I decided to make my first full-stack project about something I feel strongly about: teaching others about these little changes and their importance.

## Dependencies

### Prerequisites

Make sure you have the following installed:

- [Python] (version 3.7 or higher)
- [Node.js] (version 14 or higher)

### Backend

- **Python**
- **Flask (3.1.2)**
- **Flask_Cors (6.0.1)**
- **BeautifulSoup4 (4.13.4)**
- **OpenAI (1.101.0)**
- **Playwright (1.46.0)**
- **Requests (2.32.5)**
- **Redis (6.4.0)**

### Frontend

- **React (18.3.1) and React DOM (18.3.1)**
- **@mui/material (6.0.2) and @mui/icons-material (6.0.2)**
- **@emotion/react (11.13.3) and @emotion/styled (11.13.0)**
- **Axios (1.7.2)**
- **React Spinners (0.14.1)**

### Development Dependencies

- **Vite (5.3.4)**
- **ESLint (8.57.0)** and plugins
- **@vitejs/plugin-react (4.3.1)**

## How to Install and Run

### Backend

1. **Clone the repository**:

   ```bash
   git clone https://github.com/jrremy/semantifyHTML
   cd semantifyHTML
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the backend dependencies**:

   ```bash
   pip install -r server/requirements.txt
   ```

5. **Set the OpenAI API key (optional)**:
   You can set an environment variable for your OpenAI API key if you wish to use the explanation feature. In your terminal, run:

   - On Windows:
     ```bash
     set OPENAI_API_KEY=your_api_key_here
     ```
   - On macOS/Linux:
     ```bash
     export OPENAI_API_KEY=your_api_key_here
     ```

6. **Run Redis server (optional)**:
   If you want to use Redis for optimized explanations, make sure Redis is installed on your machine and run:

   ```bash
   redis-server
   ```

7. **Run the Flask backend**:
   ```bash
   python app.py
   ```

### Frontend

1. **Navigate to the client directory**:

   ```bash
   cd client
   ```

2. **Install the frontend dependencies**:

   ```bash
   npm install
   ```

3. **Run the Vite development server**:
   ```bash
   npm run dev
   ```

Now you should have both the backend and frontend running. Access the frontend through your web browser at `http://localhost:3000` and the backend at `http://localhost:8080`.
