import os
import json
import unittest
from markdown_converter.markdown_converter import MarkdownConverter

class TestMarkdownConverter(unittest.TestCase):
    def setUp(self):
        # Create a sample markdown file for testing
        self.sample_md_content = "# Sample Title\n\nThis is a sample markdown content."
        self.sample_md_file = "sample_test.md"
        with open(self.sample_md_file, "w") as f:
            f.write(self.sample_md_content)

    def tearDown(self):
        # Clean up the sample markdown file and JSON output
        if os.path.exists(self.sample_md_file):
            os.remove(self.sample_md_file)
        if os.path.exists("sample_test.json"):
            os.remove("sample_test.json")

    def test_convert_to_json(self):
        # Test conversion to JSON without saving to database
        converter = MarkdownConverter(self.sample_md_file, save_to_db=False)
        output_path = converter.convert()
        self.assertTrue(os.path.exists(output_path))

        with open(output_path, "r") as f:
            data = json.load(f)
            self.assertIn("sample_test.md", data)
            self.assertEqual(data["sample_test.md"][0]["title"], "Sample Title")

    def test_convert_to_json_with_db(self):
        # Test conversion to JSON with saving to database
        # Note: This test assumes a valid database connection is available
        converter = MarkdownConverter(self.sample_md_file, save_to_db=True)
        output_path = converter.convert()
        self.assertTrue(os.path.exists(output_path))

        with open(output_path, "r") as f:
                                    "content": "To create a streamlined process that allows social media influencers who specialize in car promotions to collaborate with car sellers through the marketplace app, benefiting all parties involved.",
                                    "level": 3,
                                    "children": []
                                },
                                {
                                    "title": "Steps",
                                    "content": "1. **Influencer Authorization**\n- **Step 1**: Influencers authorize their WhatsApp and social media accounts (Instagram, Facebook) with the marketplace app.\n2. **Seller Engagement**\n- **Step 2**: A car seller contacts the influencer to promote their car.\n- **Step 3**: The system initiates the promotion process.\n3. **Payment Processing**\n- **Step 4**: The system generates a payment link and sends it to the car seller via the influencer's WhatsApp.\n- **Step 5**: The car seller completes the payment.\n- **Payment Split**: The payment is automatically split between the marketplace and the influencer based on an agreed percentage.\n4. **Confirmation Notifications**\n- **Step 6**: The system sends payment confirmation messages to both the influencer and the car seller via WhatsApp.\n5. **Content Validation and Enhancement**\n- **Step 7**: The system validates and enhances the car images and text provided by the seller.\n6. **Ad Content Creation**\n- **Step 8**: The system crafts the ad content, ensuring it aligns with the influencer's style and standards.\n7. **Social Media Posting**\n- **Step 9**: The system posts the enhanced ad content to the influencer's authorized social media accounts.\n- **Optional**: The system can also promote the same ad in the marketplace.",
                                    "level": 3,
                                    "children": []
                                },
                                {
                                    "title": "Summary",
                                    "content": "- Influencers and sellers collaborate through a systematized process.\n- Payments are handled securely and fairly.\n- Content is optimized for quality and influencer branding.\n- Listings reach a broader audience via social media channels.\n---",
                                    "level": 3,
                                    "children": []
                                }
                            ]
                        },
                        {
                            "title": "2. Marketplace Car Ads Seller Posting Method",
                            "content": "",
                            "level": 2,
                            "children": [
                                {
                                    "title": "Objective",
                                    "content": "To enable direct car sellers to easily and efficiently list their cars on the marketplace, leveraging AI technology for a seamless experience.",
                                    "level": 3,
                                    "children": []
                                },
                                {
                                    "title": "Steps",
                                    "content": "1. **Listing Submission**\n- **Step 1**: Sellers visit the website or mobile app to submit a new AI-powered car listing.\n2. **Information Input Options**\n- **Option 1**: **Upload Images and Registration Card**\n- **Step 2.1**: Upload car images and registration documents.\n- **AI Processing**:\n- Extracts car details and seller information.\n- Stores data in the database.\n- Enhances images (cropping, quality adjustment).\n- **Option 2**: **Manual Entry**\n- **Step 2.2**: Seller manually inputs all required information into the listing form.\n3. **Content Validation**\n- **Step 3**: System validates images and text to ensure they are appropriate and free of watermarks.\n4. **Addition of Unique Car Information**\n- **Step 4**: Seller provides additional details such as:\n- Interior colors\n- Engine condition\n- Mileage\n- Damage status\n- Dealer reports\n- History and test results\n5. **Final Approval**\n- **Step 5**: Seller reviews and approves all listing information.\n6. **Seller Verification**\n- **Step 6**: System requires verification through:\n- Email confirmation\n- Phone number validation\n- ID verification (if necessary)\n7. **Package Selection**\n- **Step 7**: Seller chooses a listing package:\n- Free\n- Paid\n- Trial (configurable via admin panel)\n8. **Payment Processing**\n- **Step 8**: Seller completes payment for the selected package.\n9. **Listing Publication**\n- **Step 9**: System posts the approved listing on the marketplace.\n10. **Browsing and Search**\n- **Step 10**: Users can browse listings using:\n- Basic search\n- Advanced search (with customizable filters)",
                                    "level": 3,
                                    "children": []
                                },
                                {
                                    "title": "Summary",
                                    "content": "- Sellers have flexible options for listing their cars.\n- The system ensures high-quality, accurate listings.\n- Verification processes enhance trust and security.\n- Multiple package options cater to different seller needs.\n- Advanced search improves buyer experience.\n---",
                                    "level": 3,
                                    "children": []
                                }
                            ]
                        },
                        {
                            "title": "3. Automated Car Ads Posting from Populated Lists and WhatsApp",
                            "content": "",
                            "level": 2,
                            "children": [
                                {
                                    "title": "Objective",
                                    "content": "To expand the marketplace's listings by automatically sourcing car ads from influencers' social media accounts and engaging with sellers to promote their cars on the platform.",
                                    "level": 3,
                                    "children": []
                                },
                                {
                                    "title": "Steps",
                                    "content": "1. **Influencer Accounts Database**\n- **Step 1**: Influencer social media accounts are stored in the system via an upload feature.\n2. **Data Extraction**\n- **Step 2**: System crawls these accounts to extract car ads.\n- **Data Collected**:\n- Seller's social account ID\n- Contact information\n- Post images\n- Car details\n- Post text\n3. **AI Processing**\n- **Step 3**: AI enhances images and text.\n- **Classification**:\n- Car type\n- Model\n- Other relevant details\n- **Data Storage**: All information is stored in the database.\n4. **Seller Outreach**\n- **Step 4**: System sends personalized messages to sellers via WhatsApp or social media messaging, offering to promote their car on the marketplace.\n- Messages are tailored based on the car's classification.\n5. **Promotion Strategy Based on Criteria**\n- **Step 5**: System decides promotion channels based on car characteristics:\n- **Luxury Cars**: Promoted on both social media and the marketplace.\n- **Economic/Older Cars**: Promoted primarily on the marketplace.\n6. **Authorization and Validation**\n- **Step 6**: Upon seller's approval, system validates images to ensure quality.\n7. **Addition of Unique Car Information**\n- **Step 7**: Seller provides additional car details as in previous methods.\n8. **Final Approval**\n- **Step 8**: Seller reviews and approves the listing content.\n9. **Seller Verification**\n- **Step 9**: Verification processes are completed.\n10. **Package Selection**\n- **Step 10**: Seller selects a listing package.\n11. **Payment Processing**\n- **Step 11**: Payment is processed and confirmed.\n12. **Listing Publication**\n- **Step 12**: Listing is published on the marketplace and, if applicable, on social media accounts.\n13. **Notifications and Reminders**\n- **Step 13**: Seller receives confirmation messages with links to their listings.\n- **Renewal Reminders**: System sends notifications before package expiration.",
                                    "level": 3,
                                    "children": []
                                },
                                {
                                    "title": "Summary",
                                    "content": "- Automates the expansion of marketplace listings.\n- Engages sellers proactively.\n- Tailors promotion strategies based on car attributes.\n- Maintains high-quality standards through validation.\n---",
                                    "level": 3,
                                    "children": []
                                }
                            ]
                        },
                        {
                            "title": "4. Unique Enhancement Idea",
                            "content": "",
                            "level": 2,
                            "children": [
                                {
                                    "title": "Integration of AI-Driven Personalized Marketing and Analytics",
                                    "content": "To make this idea even more effective, integrate an AI-driven personalized marketing and analytics module that benefits both sellers and buyers.",
                                    "level": 3,
                                    "children": [
                                        {
                                            "title": "Features",
                                            "content": "1. **For Sellers**:\n- **Dynamic Pricing Suggestions**:\n- AI analyzes market trends, demand, and similar listings to suggest optimal pricing.\n- **Performance Analytics**:\n- Real-time insights on listing views, inquiries, and engagement.\n- **Targeted Promotion Recommendations**:\n- Suggestions on promotion strategies based on buyer behavior data.\n2. **For Buyers**:\n- **Personalized Recommendations**:\n- AI recommends cars based on browsing history, preferences, and previous interactions.\n- **Virtual Assistant**:\n- A chatbot feature that answers queries, schedules test drives, and provides additional information.\n- **Augmented Reality Previews** (if applicable):\n- Allows buyers to visualize the car in different settings or colors.",
                                            "level": 4,
                                            "children": []
                                        }
                                    ]
                                },
                                {
                                    "title": "Benefits",
                                    "content": "- **Enhanced User Experience**:\n- Personalization increases engagement and satisfaction.\n- **Data-Driven Decisions**:\n- Sellers can make informed choices on pricing and promotions.\n- **Competitive Advantage**:\n- Advanced features set the marketplace apart from competitors.\n---",
                                    "level": 3,
                                    "children": []
                                }
                            ]
                        },
                        {
                            "title": "5. Conclusion",
                            "content": "By logically organizing and integrating these methods, the car marketplace application delivers a unified and purpose-driven platform. The inclusion of AI technologies not only streamlines processes but also adds significant value for influencers, sellers, and buyers. The unique idea of integrating personalized marketing and analytics further enhances the platform's effectiveness, making it a comprehensive solution in the car marketplace industry.\n---\n**Note**: All features and processes are configurable and can be managed through the admin panel, allowing flexibility and scalability as the marketplace grows.",
                            "level": 2,
                            "children": []
                        }
                    ]
                }
            ]
        }
        
        self.assertDictEqual(actual_content, expected_content)

if __name__ == '__main__':
    unittest.main()
