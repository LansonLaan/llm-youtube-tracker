import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from jinja2 import Template

# Try to import YouTube API
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YT_AVAILABLE = True
except:
    YT_AVAILABLE = False
    print("⚠️ youtube-transcript-api not available")

@dataclass
class VideoAnalysis:
    video_id: str
    channel_name: str
    title: str
    publish_date: str
    speaker: str
    topics: List[str]
    key_points: str
    relation_to_other_channels: str
    url: str
    transcript_sample: str
    analyzed_at: str

class YouTubeLLMTracker:
    def __init__(self, openai_api_key: str = None):
        self.channels = {
            "Andrej Karpathy": "https://www.youtube.com/@AndrejKarpathy",
            "3Blue1Brown": "https://www.youtube.com/@3blue1brown",
            "Dwarkesh Patel": "https://www.youtube.com/@DwarkeshPatel",
        }
        self.use_llm = False  # Keep as mock for now
    
    def get_video_transcript(self, video_id: str) -> Optional[str]:
        """Extract transcript from YouTube video"""
        if not YT_AVAILABLE:
            return None
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            full_text = ' '.join([segment['text'] for segment in transcript_list])
            return full_text[:3000]  # Limit length
        except Exception as e:
            print(f"  No transcript: {e}")
            return None
    
    def analyze_video(self, title: str, channel: str, transcript: str) -> Dict:
        """Mock analysis (or use real LLM)"""
        # This is mock data - in production you'd call OpenAI
        topics_map = {
            "Andrej Karpathy": ["Neural Networks", "GPT Architecture", "Training LLMs"],
            "3Blue1Brown": ["Attention Mechanism", "Transformer Math", "Visualization"],
            "Dwarkesh Patel": ["AI Safety", "Scaling Laws", "Industry Interviews"]
        }
        
        key_points_map = {
            "Andrej Karpathy": "Shows how to build GPT from scratch, explaining tokenization, attention, and training loops.",
            "3Blue1Brown": "Visualizes how transformers process information, focusing on the attention mechanism mathematically.",
            "Dwarkesh Patel": "Interviews leading researchers about AGI timelines and alignment challenges."
        }
        
        relation_map = {
            "Andrej Karpathy": "Karpathy's implementation approach complements 3Blue1Brown's theory. Both cited by Dwarkesh's guests.",
            "3Blue1Brown": "Provides mathematical foundation for Karpathy's code. Often referenced in Dwarkesh interviews.",
            "Dwarkesh Patel": "Connects theory (3Blue1Brown) and practice (Karpathy) through high-level researcher discussions."
        }
        
        return {
            "speaker": channel,
            "topics": topics_map.get(channel, ["LLMs", "AI Research"]),
            "key_points": key_points_map.get(channel, "Discusses LLM developments."),
            "relation": relation_map.get(channel, "Related to broader LLM ecosystem.")
        }
    
    def generate_html_table(self, analyses: List[VideoAnalysis]) -> str:
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>LLM YouTube Landscape Tracker</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .container {
                    max-width: 1400px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 16px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    overflow: hidden;
                }
                .header {
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }
                .header h1 { font-size: 2em; margin-bottom: 10px; }
                .last-updated { color: #a0a0a0; font-size: 0.9em; }
                table { width: 100%; border-collapse: collapse; }
                th {
                    background: #f8f9fa;
                    padding: 15px;
                    text-align: left;
                    font-weight: 600;
                    color: #1a1a2e;
                    border-bottom: 2px solid #e0e0e0;
                }
                td {
                    padding: 15px;
                    border-bottom: 1px solid #e0e0e0;
                    vertical-align: top;
                }
                tr:hover { background: #f8f9fa; }
                .video-title {
                    font-weight: 600;
                    color: #667eea;
                    text-decoration: none;
                }
                .video-title:hover { text-decoration: underline; }
                .topics { display: flex; flex-wrap: wrap; gap: 5px; }
                .topic-tag {
                    background: #e0e7ff;
                    color: #4338ca;
                    padding: 4px 8px;
                    border-radius: 12px;
                    font-size: 0.75em;
                    font-weight: 500;
                }
                .speaker { font-weight: 600; color: #059669; }
                .relation { font-size: 0.9em; color: #6b7280; font-style: italic; }
                .footer {
                    background: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #6b7280;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 LLM YouTube Landscape Tracker</h1>
                    <p>What top creators actually say about Large Language Models</p>
                    <div class="last-updated">Last Updated: {{ last_updated }}</div>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Channel & Speaker</th>
                            <th>Video</th>
                            <th>Topics Covered</th>
                            <th>Key Points from Video</th>
                            <th>Relationship to Other Channels</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for video in videos %}
                        <tr>
                            <td data-label="Speaker">
                                <div class="speaker">{{ video.speaker }}</div>
                                <div style="font-size: 0.8em; color: #6b7280;">{{ video.channel_name }}</div>
                            </td>
                            <td data-label="Video">
                                <a href="{{ video.url }}" class="video-title" target="_blank">{{ video.title }}</a>
                                <div style="font-size: 0.75em; color: #9ca3af; margin-top: 5px;">{{ video.publish_date }}</div>
                            </td>
                            <td data-label="Topics">
                                <div class="topics">
                                    {% for topic in video.topics %}
                                    <span class="topic-tag">{{ topic }}</span>
                                    {% endfor %}
                                </div>
                            </td>
                            <td data-label="Key Points" style="max-width: 300px;">{{ video.key_points }}</td>
                            <td data-label="Relationships" class="relation">{{ video.relation_to_other_channels }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                <div class="footer">
                    <p>🔍 Tracks: Andrej Karpathy, 3Blue1Brown, Dwarkesh Patel</p>
                    <p>🔄 Auto-updates every hour via GitHub Actions</p>
                </div>
            </div>
        </body>
        </html>
        """
        template = Template(html_template)
        return template.render(videos=analyses, last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def run(self, video_ids: Dict[str, str]):
        analyses = []
        for channel, video_id in video_ids.items():
            print(f"Processing {channel}...")
            transcript = self.get_video_transcript(video_id)
            analysis = self.analyze_video(f"Video about LLMs", channel, transcript or "")
            
            video_analysis = VideoAnalysis(
                video_id=video_id,
                channel_name=channel,
                title=f"Latest: {channel} discusses LLM development",
                publish_date=datetime.now().strftime("%Y-%m-%d"),
                speaker=analysis.get("speaker", channel),
                topics=analysis.get("topics", ["LLMs"]),
                key_points=analysis.get("key_points", "Analysis in progress..."),
                relation_to_other_channels=analysis.get("relation", "Related to LLM ecosystem"),
                url=f"https://youtube.com/watch?v={video_id}",
                transcript_sample=transcript[:500] if transcript else "",
                analyzed_at=datetime.now().isoformat()
            )
            analyses.append(video_analysis)
        
        html_output = self.generate_html_table(analyses)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"✅ Generated index.html with {len(analyses)} videos")

if __name__ == "__main__":
    SAMPLE_VIDEOS = {
        "Andrej Karpathy": "kaMKInkV7Vs",
        "3Blue1Brown": "aircAruvnKk",
        "Dwarkesh Patel": "c2fYQHzY3Dw",
    }
    tracker = YouTubeLLMTracker(openai_api_key=None)
    tracker.run(SAMPLE_VIDEOS)
    print("🌐 Open index.html in your browser")
