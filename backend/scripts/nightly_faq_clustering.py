#!/usr/bin/env python3
"""
Nightly FAQ Clustering Script

This script runs nightly to organize and cluster FAQs for better search and organization.
It uses semantic similarity to group related FAQs and identify gaps in knowledge.
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import List, Dict, Any
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.db import get_db, FAQ, FAQCategory
from services.openai import extract_entities, analyze_sentiment


class FAQClusterer:
    """Handles FAQ clustering and organization"""
    
    def __init__(self):
        self.clusters = []
        self.gaps = []
    
    async def load_faqs(self, db) -> List[FAQ]:
        """Load all FAQs from database"""
        return db.query(FAQ).all()
    
    async def analyze_faq_content(self, faq: FAQ) -> Dict[str, Any]:
        """Analyze FAQ content for clustering"""
        try:
            # Extract entities
            entities = await extract_entities(faq.question + " " + faq.answer)
            
            # Analyze sentiment
            sentiment = await analyze_sentiment(faq.question + " " + faq.answer)
            
            return {
                "id": faq.id,
                "question": faq.question,
                "answer": faq.answer,
                "category": faq.category,
                "entities": entities,
                "sentiment": sentiment,
                "priority": faq.priority
            }
        except Exception as e:
            print(f"Error analyzing FAQ {faq.id}: {str(e)}")
            return None
    
    async def create_clusters(self, faqs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create clusters based on semantic similarity"""
        # TODO: Implement semantic clustering algorithm
        # For now, group by category and entities
        clusters = {}
        
        for faq in faqs:
            if not faq:
                continue
                
            category = faq["category"]
            if category not in clusters:
                clusters[category] = []
            
            clusters[category].append(faq)
        
        return [
            {
                "name": category,
                "faqs": faqs,
                "count": len(faqs),
                "avg_priority": sum(f["priority"] for f in faqs) / len(faqs)
            }
            for category, faqs in clusters.items()
        ]
    
    async def identify_gaps(self, clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify gaps in FAQ coverage"""
        gaps = []
        
        # Check for categories with few FAQs
        for cluster in clusters:
            if cluster["count"] < 3:
                gaps.append({
                    "type": "low_coverage",
                    "category": cluster["name"],
                    "current_count": cluster["count"],
                    "recommended_min": 5,
                    "description": f"Category '{cluster['name']}' has only {cluster['count']} FAQs"
                })
        
        # Check for high-priority categories with low priority FAQs
        for cluster in clusters:
            if cluster["avg_priority"] < 2 and cluster["count"] > 5:
                gaps.append({
                    "type": "low_priority",
                    "category": cluster["name"],
                    "avg_priority": cluster["avg_priority"],
                    "description": f"Category '{cluster['name']}' has low priority FAQs"
                })
        
        return gaps
    
    async def generate_recommendations(self, gaps: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on gaps"""
        recommendations = []
        
        for gap in gaps:
            if gap["type"] == "low_coverage":
                recommendations.append(
                    f"Add more FAQs to category '{gap['category']}' "
                    f"(currently {gap['current_count']}, recommend {gap['recommended_min']})"
                )
            elif gap["type"] == "low_priority":
                recommendations.append(
                    f"Review and prioritize FAQs in category '{gap['category']}' "
                    f"(average priority: {gap['avg_priority']:.1f})"
                )
        
        return recommendations
    
    async def run_clustering(self):
        """Run the complete clustering process"""
        print(f"Starting FAQ clustering at {datetime.now()}")
        
        try:
            # Get database session
            db = next(get_db())
            
            # Load FAQs
            print("Loading FAQs from database...")
            faqs = await self.load_faqs(db)
            print(f"Loaded {len(faqs)} FAQs")
            
            # Analyze FAQ content
            print("Analyzing FAQ content...")
            analyzed_faqs = []
            for faq in faqs:
                analysis = await self.analyze_faq_content(faq)
                if analysis:
                    analyzed_faqs.append(analysis)
            
            # Create clusters
            print("Creating clusters...")
            self.clusters = await self.create_clusters(analyzed_faqs)
            print(f"Created {len(self.clusters)} clusters")
            
            # Identify gaps
            print("Identifying gaps...")
            self.gaps = await self.identify_gaps(self.clusters)
            print(f"Identified {len(self.gaps)} gaps")
            
            # Generate recommendations
            print("Generating recommendations...")
            recommendations = await self.generate_recommendations(self.gaps)
            
            # Save results
            await self.save_results(recommendations)
            
            print("FAQ clustering completed successfully!")
            
        except Exception as e:
            print(f"Error during clustering: {str(e)}")
            raise
    
    async def save_results(self, recommendations: List[str]):
        """Save clustering results"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "clusters": self.clusters,
            "gaps": self.gaps,
            "recommendations": recommendations,
            "summary": {
                "total_faqs": sum(c["count"] for c in self.clusters),
                "total_clusters": len(self.clusters),
                "total_gaps": len(self.gaps)
            }
        }
        
        # Save to file
        output_file = f"clustering_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Results saved to {output_file}")


async def main():
    """Main function"""
    clusterer = FAQClusterer()
    await clusterer.run_clustering()


if __name__ == "__main__":
    asyncio.run(main()) 