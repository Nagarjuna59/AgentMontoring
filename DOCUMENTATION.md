# AgentMonitor - Complete Documentation

## Project Overview

AgentMonitor is a Multi-Agent System (MAS) for code generation with quality prediction and monitoring capabilities. It uses XGBoost ML models to predict code quality and provides detailed agent-level analytics.

## Features

### Core Capabilities
1. **Multi-Agent Code Generation** - 4 specialized agents collaborate
2. **Quality Prediction** - XGBoost model predicts code quality scores
3. **Agent Monitoring** - Track agent performance, scores, latency
4. **Graph Analytics** - Network analysis of agent interactions
5. **Enhancement Loops** - Iterative code improvement based on scores
6. **Language Support** - Auto-detect or specify (Python, JavaScript, Java, etc.)

### Two Operating Modes

#### ⚡ FAST MODE (Default)
- **Speed**: ~5-10 seconds
- **Agents**: Coder only
- **Features**: 10/16 populated (system + collective)
- **Graph Metrics**: 0 (expected - no graph with 1 agent)
- **Use Case**: Production, quick feedback

#### 🔬 FULL MAS MODE
- **Speed**: ~20-40 seconds
- **Agents**: Analyzer → Coder → Tester → Reviewer
- **Features**: 16/16 populated (all metrics)
- **Graph Metrics**: Non-zero (clustering, centrality, pagerank)
- **Use Case**: Research, demonstrations, comprehensive analysis

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB (local or Atlas)
- Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AgentMonitor/Final
   ```

2. **Set up Backend**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   
   # Create .env file
   echo GEMINI_API_KEY=your_key_here > .env
   echo MONGO_URI=mongodb://localhost:27017 >> .env
   ```

3. **Set up Frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Start Services**
   ```powershell
   # Use the provided script
   .\start.ps1
   
   # Or manually:
   # Terminal 1 - Backend
   cd backend
   python app.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

5. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8080
   - Default admin: admin/admin123

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│  - User Dashboard (chat interface)                          │
│  - Admin Dashboard (analytics, run details)                 │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/REST API
┌─────────────────────▼───────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  - Authentication (JWT)                                      │
│  - MAS Orchestration                                         │
│  - Feature Extraction                                        │
│  - XGBoost Prediction                                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┬─────────────────────────┐
        ▼                           ▼                         ▼
┌───────────────┐       ┌────────────────────┐    ┌──────────────┐
│   MongoDB     │       │  AgentMonitor MAS  │    │  Gemini API  │
│   Database    │       │  - CodeGeneration  │    │  (LLM)       │
│               │       │  - Enhancement     │    │              │
└───────────────┘       └────────────────────┘    └──────────────┘
```

### Agent Workflow

**FAST MODE:**
```
User Request → Coder → Code Output
```

**FULL MAS MODE:**
```
User Request → Analyzer → Coder → Tester → Reviewer → Code Output
                 ↓          ↓        ↓         ↓
              (Requirements)(Code)(Tests)(Review)
```

## Feature System

### 16 Features Extracted

#### System Features (6)
1. **avg_personal_score** - Average agent quality score
2. **min_personal_score** - Minimum agent score
3. **max_loops** - Maximum enhancement iterations
4. **total_latency** - Total execution time (seconds)
5. **total_token_usage** - Total LLM tokens consumed
6. **num_agents_triggered_enhancement** - Agents needing improvement

#### Graph Features (9)
7. **num_nodes** - Number of agents used
8. **num_edges** - Agent-to-agent interactions
9. **clustering_coefficient** - Graph clustering
10. **transitivity** - Graph transitivity
11. **avg_degree_centrality** - Node importance
12. **avg_betweenness_centrality** - Node betweenness
13. **avg_closeness_centrality** - Node closeness
14. **pagerank_entropy** - PageRank distribution
15. **heterogeneity_score** - Graph variance

#### Collective Feature (1)
16. **collective_score** - Overall system quality

### Feature Values by Mode

| Feature Type | FAST MODE | FULL MAS MODE |
|--------------|-----------|---------------|
| System (6) | ✅ All values | ✅ All values |
| Graph (9) | ⚠️ Mostly 0* | ✅ All values |
| Collective (1) | ✅ Value | ✅ Value |

*num_nodes=1, num_edges=0, others=0 (mathematically correct)

## User Guide

### Using FAST MODE (Default)

1. Login to user dashboard
2. Enter coding task: "Write a function to sort an array"
3. Click "🚀 Run MAS"
4. Wait ~10 seconds
5. View initial code immediately
6. Enhanced code loads in background

### Using FULL MAS MODE (For Complete Analysis)

1. Login to user dashboard
2. **Check the toggle**: ☑ 🔬 Full MAS Mode (4 agents + graph metrics)
3. Enter coding task
4. Click "🚀 Run MAS"
5. Wait ~30-40 seconds
6. View comprehensive results

**When to use Full MAS Mode:**
- Research demonstrations
- Comprehensive quality analysis
- Need all 16 features populated
- Want to see multi-agent collaboration
- Require graph metrics (clustering, centrality, etc.)

### Admin Features

1. **View All Runs** - See all user submissions
2. **Run Details** - Complete analysis with:
   - MAS Indicators (16 features)
   - Per-Agent Breakdown (scores, latency, tokens)
   - Code comparison (initial vs enhanced)
   - Predicted quality score

3. **Filter/Search** - Find specific runs by user, date, score

## API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - User registration

### Code Generation
- `POST /api/run-mas-start` - Start MAS run (returns initial code)
- `GET /api/run/{run_id}` - Get run details (polls for enhanced code)

### Data Access
- `GET /api/runs/user` - Get user's runs
- `GET /api/runs/all` - Get all runs (admin only)

## Configuration

### Environment Variables

**Backend (.env):**
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY_2=optional_second_key
GEMINI_API_KEY_3=optional_third_key
MONGO_URI=mongodb://localhost:27017
SECRET_KEY=your_jwt_secret_key
```

**Frontend:**
- API URL configured in `src/api.js` (default: http://localhost:8080/api)

### Customization

**Adjust MAS Parameters** (backend/app.py):
```python
# FAST MODE (initial)
mas_initial = CodeGenerationMAS(
    llm=llm,
    language='auto',
    threshold=1.0,      # No enhancement
    max_retries=0,
    use_full_mas=False  # Single agent
)

# Enhancement (background)
mas_enhanced = CodeGenerationMAS(
    llm=llm,
    language=language,
    threshold=0.75,     # Quality threshold
    max_retries=1,      # Enhancement attempts
    use_full_mas=use_full_mas  # User's choice
)
```

## Troubleshooting

### Graph Metrics Show 0

**Symptom:** Admin view shows 0 for clustering, centrality, etc.

**Cause:** Run used FAST MODE (1 agent only)

**Solution:** Enable "🔬 Full MAS Mode" toggle in user dashboard

**Why:** Graph metrics require multiple nodes (agents). 1 agent = no graph = metrics = 0 (mathematically correct)

### Frontend Not Showing Toggle

**Solution:**
1. Hard refresh: Ctrl + Shift + R
2. Restart frontend: `npm start`
3. Clear browser cache

### Backend Errors

**Common Issues:**
1. **MongoDB connection failed** - Check MONGO_URI, ensure MongoDB running
2. **Gemini API key invalid** - Verify GEMINI_API_KEY in .env
3. **Port 8080 in use** - Kill process or change port

### Enhancement Not Working

**Check:**
1. Monitor data populated? (backend logs show "Monitor data keys: ...")
2. Threshold too high? (lower to 0.75)
3. Max retries = 0? (increase to 1-2)

## Development

### Project Structure

```
Final/
├── backend/
│   ├── app.py              # Main FastAPI server
│   ├── database.py         # MongoDB operations
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── UserDashboard.js
│   │   │   ├── AdminDashboard.js
│   │   │   └── AdminPromptDetail.js
│   │   ├── api.js
│   │   └── App.js
│   └── package.json
├── AgentMonitor/
│   ├── core/
│   │   └── enhanced_monitor.py
│   ├── mas/
│   │   └── code_generation_mas.py
│   ├── features/
│   │   └── feature_extractor.py
│   └── gemini_api.py
└── README.md
```

### Adding New Features

1. **Update Feature Extraction** (backend/app.py)
   ```python
   def extract_features_from_monitor(monitor_data: dict) -> dict:
       # Add your feature calculation
       features["new_feature"] = calculate_new_feature(monitor_data)
       return features
   ```

2. **Update Frontend Display** (frontend/src/pages/AdminPromptDetail.js)
   ```javascript
   const masIndicators = [
       { name: "New Feature", key: "new_feature" },
       // ... existing features
   ];
   ```

3. **Retrain XGBoost Model** if feature affects predictions

### Testing

**Backend Tests:**
```bash
cd backend
python -m pytest tests/
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

**End-to-End Test:**
1. Enable Full MAS Mode
2. Submit: "Write fibonacci function"
3. Verify in admin:
   - num_nodes = 4
   - num_edges = 3
   - All graph metrics non-zero

## Performance Optimization

### Speed vs Quality Trade-off

| Priority | Mode | Time | Features | Quality |
|----------|------|------|----------|---------|
| Speed | FAST | ~10s | 10/16 | Good |
| Quality | FULL | ~40s | 16/16 | Excellent |

### Caching Strategies

- Frontend caches user runs
- Backend uses connection pooling
- MongoDB indexes on user_id, created_at

### Scaling Considerations

1. **Horizontal Scaling** - Run multiple backend instances
2. **Load Balancing** - Nginx/HAProxy for backend
3. **Database** - MongoDB Atlas for managed scaling
4. **API Rate Limiting** - Implement per-user quotas

## Research Applications

### Multi-Agent Collaboration Analysis

Full MAS Mode enables research on:
- Agent interaction patterns
- Collaboration efficiency
- Graph topology effects on quality
- Optimal agent sequences

### Metrics for Research

```python
# Example: Analyze agent collaboration
graph_edges = [
    ["Analyzer", "Coder"],
    ["Coder", "Tester"],
    ["Tester", "Reviewer"]
]

# NetworkX analysis
G = nx.DiGraph()
G.add_edges_from(graph_edges)
clustering = nx.clustering(G.to_undirected())
centrality = nx.betweenness_centrality(G)
```

### Publications

Potential research directions:
- Multi-agent code generation effectiveness
- Quality prediction using graph metrics
- Agent orchestration optimization
- LLM collaboration patterns

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## License

[Specify your license]

## Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Documentation: This file
- Email: [contact-email]

## Changelog

### Version 1.0 (Current)
- ✅ Full MAS Mode implementation
- ✅ Capability bug fix (auto/python/java display)
- ✅ 16-feature extraction system
- ✅ Graph metrics calculation
- ✅ ChatGPT-like UI
- ✅ Two-step workflow (initial + enhancement)
- ✅ Admin analytics dashboard

### Known Issues
- None currently

### Roadmap
- [ ] Additional language support
- [ ] Custom agent configurations
- [ ] Real-time agent progress tracking
- [ ] Graph visualization
- [ ] Export features to CSV
- [ ] API rate limiting
- [ ] User quotas

---

**Last Updated:** October 2025

**Version:** 1.0

**Status:** Production Ready ✅
