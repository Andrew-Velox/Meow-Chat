# 🚀 Meow Chat - Discord-Style Real-Time Chat Application

A modern, feature-rich real-time chat application built with Django and WebSockets, featuring a sleek Discord-inspired user interface.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Django](https://img.shields.io/badge/Django-5.2%2B-green)
![WebSockets](https://img.shields.io/badge/WebSockets-Enabled-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🎨 **Modern Discord-Style UI**
- Clean, dark theme with Discord color palette
- Responsive design for all devices
- Smooth animations and hover effects
- Professional card-based layouts

### 💬 **Real-Time Chat**
- Instant messaging with WebSocket connections
- Multiple chat rooms and private messaging
- File sharing with drag & drop support
- Message history and pagination
- Typing indicators and message reactions

### 👥 **User Management**
- User authentication with Django Allauth
- Custom user profiles with avatars
- Online/offline status indicators
- Profile editing and settings management

### 🛡️ **Security & Validation**
- CSRF protection
- Message content validation
- File upload restrictions
- User permission management
- Email verification system

### 📱 **Advanced Features**
- **Smart Sidebar Navigation**: Server-style sidebar with chat organization
- **Online Status System**: Real-time user presence indicators
- **File Preview System**: Visual file attachment previews
- **Admin Controls**: Channel management and moderation
- **Responsive Design**: Mobile-friendly interface

## 🛠️ Technology Stack

### Backend
- **Django 5.2+** - Web framework
- **Django Channels** - WebSocket support
- **Django Allauth** - Authentication system
- **SQLite** - Database (easily configurable for PostgreSQL/MySQL)
- **Redis** (optional) - Channel layer backend

### Frontend
- **HTML5 & CSS3** - Modern web standards
- **JavaScript (ES6+)** - Interactive functionality
- **TailwindCSS** - Utility-first CSS framework
- **HTMX** - Dynamic HTML updates
- **AlpineJS** - Lightweight JavaScript framework

### Real-Time
- **WebSockets** - Bidirectional communication
- **ASGI** - Asynchronous server interface
- **Daphne** - ASGI server

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Andrew-Velox/Meow-Chat.git
   cd Meow-Chat
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   # Create .env file (optional)
   cp .env.example .env
   
   # Edit .env with your configurations
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000`
   - Create an account or use existing credentials

## 📁 Project Structure

```
Meow-Chat/
│
├── a_core/                 # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL routing
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
│
├── a_home/                 # Home app
│   ├── views.py            # Home views
│   └── models.py           # Home models
│
├── a_rtchat/               # Real-time chat app
│   ├── models.py           # Chat models (ChatGroup, GroupMessage)
│   ├── views.py            # Chat views
│   ├── consumers.py        # WebSocket consumers
│   ├── routing.py          # WebSocket routing
│   ├── forms.py            # Chat forms
│   └── templates/          # Chat templates
│
├── a_users/                # User management app
│   ├── models.py           # User profile models
│   ├── views.py            # User views
│   ├── forms.py            # User forms
│   └── templates/          # User templates
│
├── templates/              # Global templates
│   ├── base.html           # Base template with Discord styling
│   ├── includes/           # Reusable components
│   └── layouts/            # Layout templates
│
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User-uploaded files
└── requirements.txt        # Python dependencies
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (optional - uses SQLite by default)
DATABASE_URL=postgresql://user:password@localhost:5432/meowchat

# Email settings (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Cloudinary (for file storage - optional)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Redis (for production WebSocket scaling - optional)
REDIS_URL=redis://localhost:6379/0
```

### Production Deployment

For production deployment, consider:

1. **Use PostgreSQL** instead of SQLite
2. **Setup Redis** for channel layers
3. **Configure proper static file serving** (WhiteNoise/CloudFront)
4. **Enable HTTPS** for WebSocket security
5. **Setup proper logging** and monitoring

## 🎯 Usage Guide

### Creating Chat Rooms

1. **Public Rooms**: Accessible to all users
2. **Private Rooms**: Invite-only with member management
3. **Direct Messages**: One-on-one conversations

### User Features

- **Profile Management**: Update avatar, display name, and bio
- **Account Settings**: Change email, username, and security settings
- **Online Status**: Real-time presence indicators
- **File Sharing**: Upload and share files with preview

### Admin Features

- **Room Management**: Create, edit, and delete chat rooms
- **User Moderation**: Manage room members and permissions
- **Content Management**: Monitor and moderate chat content

## 🔧 Development

### Running in Development Mode

```bash
# Start the development server
python manage.py runserver

# In another terminal, start the WebSocket server (if using separate process)
python manage.py runworker
```

### Code Style

This project follows:
- **PEP 8** for Python code
- **Django best practices**
- **Clean code principles**
- **Responsive design patterns**

### Testing

```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test a_rtchat
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** and follow the coding standards
4. **Write tests** for new functionality
5. **Commit your changes** (`git commit -m 'Add amazing feature'`)
6. **Push to the branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

### Development Guidelines

- Follow Django best practices
- Write clear, commented code
- Ensure responsive design
- Test WebSocket functionality
- Update documentation as needed

## 📝 API Reference

### WebSocket Endpoints

```javascript
// Chat room connection
ws://localhost:8000/ws/chatroom/{room_name}/

// Message format
{
    "body": "Your message here",
    "event": "message_create"
}
```

### REST Endpoints

- `/api/user-chats/` - Get user's chat rooms
- `/profile/{username}/` - User profile page
- `/chat/room/{room_name}/` - Chat room page
- `/chat/new_groupchat/` - Create new chat room

## 🐛 Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Check if Daphne is running
   - Verify ASGI configuration
   - Ensure proper URL routing

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check static file configuration

3. **Database Errors**
   - Run migrations: `python manage.py migrate`
   - Check database configuration

4. **Email Verification Issues**
   - Verify email settings in `.env`
   - Check spam folder for confirmation emails

### Performance Optimization

- Use Redis for channel layers in production
- Optimize database queries with select_related
- Implement proper caching strategies
- Use CDN for static file delivery

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Team** - For the amazing web framework
- **Django Channels** - For WebSocket support
- **TailwindCSS** - For the utility-first CSS framework
- **Discord** - For UI/UX inspiration
- **Open Source Community** - For the incredible tools and libraries

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Andrew-Velox/Meow-Chat/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Andrew-Velox/Meow-Chat/discussions)
- **Email**: mohabbat@example.com

## 🚀 Future Enhancements

- [ ] **Voice & Video Calls** - WebRTC integration
- [ ] **Message Encryption** - End-to-end encryption
- [ ] **Mobile App** - React Native/Flutter version
- [ ] **Bot Integration** - Chatbot and automation features
- [ ] **Advanced Moderation** - AI-powered content filtering
- [ ] **Themes & Customization** - User-customizable themes
- [ ] **Analytics Dashboard** - Usage statistics and insights

---

**Built with ❤️ by [Andrew Velox](https://github.com/Andrew-Velox)**

⭐ **Star this repository if you find it helpful!**
