# 🛡️ SafeSpace - AI-Powered Social Media Platform

A cyberbullying-proof social media platform that uses machine learning to detect and prevent harmful content in real-time.

## ✨ Features

- **AI-Powered Moderation**: Machine learning model detects cyberbullying before comments are posted
- **Real-Time Detection**: Instant analysis with confidence scores
- **Progressive Warning System**: 3-strike system before account blocking
- **User Authentication**: Secure Firebase authentication
- **Image Sharing**: Cloud-based image storage with Cloudinary
- **Responsive Design**: Modern, Instagram-style UI

## 🏗️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Firebase Realtime Database
- **Authentication**: Firebase Auth
- **Image Storage**: Cloudinary
- **ML Model**: Scikit-learn (Logistic Regression + TF-IDF)
- **Language**: Python 3.9+

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- Firebase account
- Cloudinary account

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/safespace.git
cd safespace
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Firebase:
   - Create a Firebase project
   - Download `firebase_config.py` with your credentials
   - Enable Authentication (Email/Password)
   - Enable Realtime Database

4. Configure Cloudinary:
   - Create a Cloudinary account
   - Add credentials to `cloudinary_config.py`

5. Train the ML model:
```bash
python train_model.py
```

6. Run the application:
```bash
streamlit run app.py
```

## 🚀 Deployment

Deploy to Streamlit Community Cloud:

1. Push to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets in Streamlit Cloud dashboard

## 📁 Project Structure
```
safespace/
├── app.py                      # Main application
├── modules/
│   ├── firebase_auth.py        # Authentication logic
│   ├── firebase_database.py    # Database operations
│   ├── cloudinary_upload.py    # Image upload handling
│   └── moderation.py           # Moderation controller
├── models/
│   ├── cyberbullying_classifier.pkl
│   └── tfidf_vectorizer.pkl
├── data/                       # Training datasets
├── assets/                     # Static assets
├── requirements.txt
└── README.md
```

## 🔒 Security

- All credentials stored in separate config files (not tracked by Git)
- Firebase security rules configured
- User data encrypted
- HTTPS-only in production

## 📊 ML Model

- **Algorithm**: Logistic Regression with TF-IDF vectorization
- **Accuracy**: 85-95%
- **Training Data**: 4 datasets (47,000+ labeled comments)
- **Categories**: Cyberbullying detection (binary classification)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Firebase for backend services
- Cloudinary for image hosting
- Streamlit for the amazing framework