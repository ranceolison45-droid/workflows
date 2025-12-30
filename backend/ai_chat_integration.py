"""
AI Chat Integration for StormBuster
Provides integration with multiple AI providers (OpenAI, Anthropic, Google)
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import AI SDKs
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class AIProvider(Enum):
    """AI Provider enumeration"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


class StormBusterAIChat:
    """AI Chat integration for StormBuster backend"""
    
    def __init__(self):
        """Initialize AI Chat with available providers"""
        self.providers = set()
        self.chat_history = []
        self.usage_stats = {
            "basic": {"messages": 0, "tokens": 0, "cost": 0.0},
            "premium": {"messages": 0, "tokens": 0, "cost": 0.0},
            "enterprise": {"messages": 0, "tokens": 0, "cost": 0.0}
        }
        
        # Initialize OpenAI client if available
        self.openai_client = None
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and OPENAI_AVAILABLE:
            try:
                self.openai_client = OpenAI(api_key=openai_key)
                self.providers.add(AIProvider.OPENAI)
            except Exception:
                pass
        
        # Initialize Anthropic client if available
        self.anthropic_client = None
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key and ANTHROPIC_AVAILABLE:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
                self.providers.add(AIProvider.ANTHROPIC)
            except Exception:
                pass
        
        # Check for Google API key
        if os.getenv("GOOGLE_API_KEY"):
            self.providers.add(AIProvider.GOOGLE)
    
    def get_available_models(self, tier: str = "basic") -> List[Dict[str, Any]]:
        """Get available AI models for subscription tier"""
        models = {
            "basic": [
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "openai"},
                {"id": "claude-3-haiku", "name": "Claude 3 Haiku", "provider": "anthropic"},
            ],
            "premium": [
                {"id": "gpt-4", "name": "GPT-4", "provider": "openai"},
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "openai"},
                {"id": "claude-3-opus", "name": "Claude 3 Opus", "provider": "anthropic"},
                {"id": "claude-3-sonnet", "name": "Claude 3 Sonnet", "provider": "anthropic"},
                {"id": "gemini-pro", "name": "Gemini Pro", "provider": "google"},
                {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "provider": "google"},
                {"id": "gemini-3.5-pro", "name": "Gemini 3.5 Pro", "provider": "google"},
            ],
            "enterprise": [
                {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "provider": "openai"},
                {"id": "gpt-4", "name": "GPT-4", "provider": "openai"},
                {"id": "claude-3-opus", "name": "Claude 3 Opus", "provider": "anthropic"},
                {"id": "claude-3-sonnet", "name": "Claude 3 Sonnet", "provider": "anthropic"},
                {"id": "gemini-pro", "name": "Gemini Pro", "provider": "google"},
                {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "provider": "google"},
                {"id": "gemini-3.5-pro", "name": "Gemini 3.5 Pro", "provider": "google"},
            ]
        }
        return models.get(tier, models["basic"])
    
    def send_message(
        self,
        message: str,
        model_id: str = "gpt-3.5-turbo",
        subscription_tier: str = "basic",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send a chat message to AI"""
        try:
            # Add to chat history
            chat_entry = {
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "model": model_id,
                "tier": subscription_tier,
                "context": context
            }
            self.chat_history.append(chat_entry)
            
            # Build system message with context if provided
            system_message = context if context else "You are a helpful assistant for storm damage analysis and lead generation."
            
            response_text = None
            tokens_used = 0
            cost = 0.0
            
            # Try OpenAI models
            if model_id.startswith("gpt") and self.openai_client:
                try:
                    messages = [{"role": "user", "content": message}]
                    if system_message:
                        messages.insert(0, {"role": "system", "content": system_message})
                    
                    response = self.openai_client.chat.completions.create(
                        model=model_id,
                        messages=messages
                    )
                    response_text = response.choices[0].message.content
                    tokens_used = response.usage.total_tokens
                    # Rough cost estimate (varies by model)
                    cost = tokens_used * 0.000002 if "gpt-4" in model_id else tokens_used * 0.0000005
                except Exception as e:
                    return {
                        "success": False,
                        "error": f"OpenAI API error: {str(e)}",
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Try Anthropic models
            elif model_id.startswith("claude") and self.anthropic_client:
                try:
                    # Map model IDs to Anthropic model names
                    anthropic_model_map = {
                        "claude-3": "claude-3-opus-20240229",
                        "claude-3-opus": "claude-3-opus-20240229",
                        "claude-3-sonnet": "claude-3-sonnet-20240229",
                        "claude-3-haiku": "claude-3-haiku-20240307"
                    }
                    anthropic_model = anthropic_model_map.get(model_id, "claude-3-sonnet-20240229")
                    
                    full_message = f"{system_message}\n\n{message}" if system_message else message
                    
                    response = self.anthropic_client.messages.create(
                        model=anthropic_model,
                        max_tokens=1024,
                        messages=[{"role": "user", "content": full_message}]
                    )
                    response_text = response.content[0].text
                    tokens_used = response.usage.input_tokens + response.usage.output_tokens
                    # Rough cost estimate
                    cost = tokens_used * 0.000015 if "opus" in anthropic_model else tokens_used * 0.000003
                except Exception as e:
                    return {
                        "success": False,
                        "error": f"Anthropic API error: {str(e)}",
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Fallback if no API client available
            if not response_text:
                response_text = f"AI Response to: {message[:50]}... (API not configured)"
                tokens_used = len(message.split()) * 1.3
            
            # Update usage stats
            self.usage_stats[subscription_tier]["messages"] += 1
            self.usage_stats[subscription_tier]["tokens"] += int(tokens_used)
            self.usage_stats[subscription_tier]["cost"] += cost
            
            return {
                "success": True,
                "response": response_text,
                "model_used": model_id,
                "tokens_used": int(tokens_used),
                "cost": round(cost, 6),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def analyze_storm_data(
        self,
        storm_data: Dict[str, Any],
        model_id: str = "gpt-4"
    ) -> Dict[str, Any]:
        """Analyze storm data using AI"""
        try:
            prompt = f"""Analyze the following storm data and provide insights:

Location: {storm_data.get('location', 'Unknown')}
Date: {storm_data.get('date', 'Unknown')}
Hail Size: {storm_data.get('hail_size', 'Unknown')}
Properties Affected: {storm_data.get('property_count', 0)}
Average Property Value: {storm_data.get('avg_property_value', 'Unknown')}

Please provide:
1. Key insights about the storm impact
2. Recommendations for lead generation
3. Priority areas to focus on
4. Estimated damage potential"""
            
            # Use send_message to get AI analysis
            result = self.send_message(
                message=prompt,
                model_id=model_id,
                subscription_tier="premium",
                context="You are an expert in storm damage analysis and property assessment."
            )
            
            if result.get("success"):
                # Parse the AI response into structured format
                response_text = result.get("response", "")
                return {
                    "success": True,
                    "analysis": response_text,
                    "key_insights": [
                        f"Hail size: {storm_data.get('hail_size', 'unknown')}",
                        f"Properties affected: {storm_data.get('property_count', 0)}",
                        "AI analysis completed"
                    ],
                    "recommendations": [
                        "Review AI analysis for specific recommendations",
                        "Prioritize high-value properties",
                        "Follow up within 48 hours"
                    ],
                    "model_used": model_id,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Failed to analyze storm data")
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_lead_insights(
        self,
        lead_data: Dict[str, Any],
        model_id: str = "claude-3"
    ) -> Dict[str, Any]:
        """Generate insights for individual leads"""
        try:
            prompt = f"""Generate insights for this lead:

Owner Name: {lead_data.get('owner_name', 'Unknown')}
Address: {lead_data.get('address', 'Unknown')}
Property Value: {lead_data.get('property_value', 'Unknown')}
Storm Date: {lead_data.get('storm_date', 'Unknown')}
Hail Size: {lead_data.get('hail_size', 'Unknown')}
Phone: {lead_data.get('phone', 'Not provided')}

Provide:
1. Key insights about this lead
2. Recommended approach for outreach
3. Priority level (High/Medium/Low)
4. Best time to contact"""
            
            # Use send_message to get AI insights
            result = self.send_message(
                message=prompt,
                model_id=model_id,
                subscription_tier="premium",
                context="You are an expert in lead generation and sales strategy for storm damage restoration."
            )
            
            if result.get("success"):
                response_text = result.get("response", "")
                return {
                    "success": True,
                    "lead_address": lead_data.get("address", "unknown"),
                    "insights": [
                        f"Property value: {lead_data.get('property_value', 'unknown')}",
                        f"Storm date: {lead_data.get('storm_date', 'unknown')}",
                        f"Hail size: {lead_data.get('hail_size', 'unknown')}",
                        response_text
                    ],
                    "recommended_approach": "Review AI insights for specific recommendations",
                    "model_used": model_id,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Failed to generate lead insights")
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_chat_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get chat history"""
        return self.chat_history[-limit:] if limit > 0 else self.chat_history
    
    def clear_chat_history(self) -> None:
        """Clear chat history"""
        self.chat_history = []
    
    def get_usage_stats(self, tier: str = "basic") -> Dict[str, Any]:
        """Get usage statistics"""
        return self.usage_stats.get(tier, self.usage_stats["basic"])
    
    def export_chat_history(self) -> Dict[str, Any]:
        """Export chat history as JSON"""
        return {
            "exported_at": datetime.now().isoformat(),
            "total_messages": len(self.chat_history),
            "history": self.chat_history,
            "usage_stats": self.usage_stats
        }

