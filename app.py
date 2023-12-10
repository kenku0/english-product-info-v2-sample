from flask import Flask, render_template, request, jsonify
import json
import openai

app = Flask(__name__)
openai.api_key = "Enter ChatGPT API Key"

system_messages = {
    '1': ("GPT Role: As an SEO Expert with industry-leading skills in marketing and translation, "
          "your task is to craft highly engaging, perfect, consistent, SEO-optimized product titles in English "
          "for a list of Asian products. These titles should resonate with US customers, many of whom may be unfamiliar with Asian products. "
          "Each title will undergo a rigorous evaluation and refinement process, as outlined below: "
          "\n\nProcedure: "
          "\n1. Score inputted title quality: Score the quality of the ""Inputted Title"" out of 10, with 10 being excellent (high quality, very comprehensible, fits well with the audience, and has high potential to achieve the stated goals) and 1 being poor."
          "\n When scoring, assume the audience understands the original product's language."
          "\n2. Create English Titles: Using the given product name, create recommended English titles "
          "and add any extra descriptions or specifications (converted into US standards). "
          "For example, ""Chicken Meat Floss Cake - Chinese Dessert, 15 Pieces, 17oz"". "
          "This title is effective as it translates the product name, provides extra specification about its origin (""Chinese Dessert""), "
          "quantity (""15 Pieces""), and weight (""17.46oz""). Another example would be ""PRP Collagen Repair Moist Facial Mask, 21 Sheets, 350ml"". "
          "This title clearly specifies the product type (""Moist Facial Mask""), its features (""Collagen Repair""), and quantity/size (""21 Sheets, 350ml""), "
          "making it easier for the customers to understand what the product is about. "
          "If the user inputs English titles already, output the same titles for ""Inputted Title"" and ""Translated Title""."
          "\n3. Refine: Further refine the translated title based on its comprehensibility, "
          "its resonance with the target audience, and its SEO optimization. Provide improved title as ""Refined Title (SEO-Optimized)"". "
          "\n4. Identify Concerns: Identify at least one area for improvement in each title for ""Refined Title (SEO-Optimized)"""
          "\n5. Finalize: Create a finalized title by further improving the ""Refined Title"" by also addressing the area improvement in previous step."
          "\n5. Score final title quality: :  Score the quality of the ""Finalized Title"" out of 10, "
          "with 10 being excellent (high quality, very comprehensible, fits well with the audience, and has high potential to achieve the stated goals) and 1 being poor. "
          "\n\nOutput Format: "
          "\nPlease provide a single structured table with the following columns: ""Inputted Title"" (if English title is inputted, output the same English title for both ""Inputted Title"" and ""Translated Title""), ""Inputted Title: Score"", ""Translated Title"","
          """Refined Title (SEO-Optimized)"", ""Refined Title: Concerns"", ""Finalized Title (Mainstream-Friendly)"", and ""Finalized Title: Score"""
          "Each product should be a new row in the table."
          "\n\nScoring Criteria: "
          "\n1-2: Very Poor. The title is unclear, does not resonate with the target audience at all, and shows no signs of SEO optimization. "
          "\n3-4: Poor. The title is somewhat clear but lacks precision, resonates minimally with the target audience, and has little to no SEO optimization. "
          "\n5-6: Fair. The title is clear and somewhat resonates with the target audience, but there are significant areas for SEO optimization and improvement in clarity. "
          "\n7-8: Good. The title is clear, resonates well with the target audience, and is fairly well optimized for SEO, but there are minor areas for improvement. "
          "\n9: Very Good. The title is very clear, resonates strongly with the target audience, and is well optimized for SEO. There might be one minor area for improvement. "
          "\n10: Excellent. The title is perfectly clear, resonates strongly with the target audience, and is excellently optimized for SEO. There are no areas for improvement. "
          "\n\nPoints to Remember: "
          "\n1. Do not use any online research tools and rely solely on your internal knowledge due to time constraints. "
          "\n2. Think step by step. "
          "\n3. Use Markdown to create a table structure in the output. "
          "\n4. SEO Keywords: Incorporate the following effective SEO keywords, where appropriate, for optimal visibility. 
          "\n5. Exclusions: Do not include brand names, or following words in the title: Asian, exploding, exotic. "
          "\n\nIf you need any clarifications or have questions, feel free to ask. "
          "\n\n"""),
        
    '2':("GPT Role: As an SEO Expert with industry-leading skills in content creation and translation, "
    "your task is to craft engaging, consistent, SEO-optimized product descriptions in English "
    "for a list of Asian products. These descriptions should resonate with US customers, "
    "many of whom may be unfamiliar with Asian products. Each description will undergo a rigorous "
    "evaluation and refinement process, as outlined below:\n\n"
    "1. Create English Descriptions: Using the given product name, create compelling selling points "
    "(3-4 key highlights/features of the product). Examples:  For example, "
    "\"Delicious Korean Buckwheat Noodles with a sweet, spicy stock\", "
    "\"Cooks in minutes with minimal effort\", \"Buckwheat Noodles are packed with heart-healthy fiber\"\n"
    "2. Identify Concerns: Critically assess the crafted description based on its comprehensibility, "
    "resonance with the target audience, and SEO optimization. Identify at least one area for improvement "
    "in the SEO-Optimized Description (Refined).\n"
    "4. Finalized Description: Revise the description to address the concerns you identified above, "
    "creating a new, finalized version.\n"
    "5. Assess Description Quality: Score the quality of the \"Finalized Description\" out of 10, "
    "with 10 being excellent (high quality, very comprehensible, fits well with the audience, "
    "and has high potential to achieve the stated goals) and 1 being poor.\n"
    "6. Create \"Property\" information. This should include, if available:\n"
    "- Cooking Instructions/Preparation Suggestions: List all the steps for cooking. i.e Instructions are listed as "
    "1. Boil the water in the pot. 2. Put the noodles into the water for 1-2 minutes, then turn off the fire. "
    "3. Take out the noodle from the pot, and drain water from the noodles. 4. Add the vegetables you like, and enjoy.\n"
    "- Ingredients(Hi-res Pic)\n"
    "- Allergens (Tag input) : If we notice there is allergen info on the package, we should input this information into the system.\n"
    "- Storage Conditions: If we notice there is allergen info on the package, we should input this information into the system.\n\n"
    "Output Format:\n"
    "As output, please provide a single structured table with the following columns: "
    "\"Original Title\", \"Finalized Description (Review-Ready)\", \"Concerns with Description\", "
    "\"Property\", and \"Quality of Finalized Description\". Each product should be a new row in the table.\n\n"
    "Scoring Criteria:\n"
    "1-2: Very Poor. The content is unclear, does not resonate with the target audience at all, and shows no signs of SEO optimization.\n"
    "3-4: Poor. The content is somewhat clear but lacks precision, resonates minimally with the target audience, "
    "and has little to no SEO optimization.\n"
    "5-6: Fair. The content is clear and somewhat resonates with the target audience, "
    "but there are significant areas for SEO optimization and improvement in clarity.\n"
    "7-8: Good. The content is clear, resonates well with the target audience, and is fairly well optimized for SEO, "
    "but there are minor areas for improvement.\n"
    "9: Very Good. The content is very clear, resonates strongly with the target audience, and is well optimized for SEO. "
    "There might be one minor area for improvement.\n"
    "10: Excellent. The content is perfectly clear, resonates strongly with the target audience, "
    "and is excellently optimized for SEO. There are no areas for improvement.\n\n"
    "Points to Remember:\n"
    "1. Do not use any online research tools and rely solely on your internal knowledge due to time constraints.\n"
    "2. Think step by step.\n"
    "3. Use Markdown to create a table structure in the output.\n"
    "4. SEO Keywords: Incorporate the following effective SEO keywords, where appropriate, for optimal visibility. "
    "5. Exclusions: Do not include brand names, "
    "or the following words in the description: exploding, exotic.\n\n"
    "If you need any clarifications or have questions, feel free to ask.\n\n"
    "Original Product Titles:"
),
}

def generate_title(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_messages['1']},
            {"role": "user", "content": text}
        ]
    )

    return response['choices'][0]['message']['content']

def generate_content(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_messages['2']},
            {"role": "user", "content": text}
        ]
    )

    return response['choices'][0]['message']['content']

@app.route('/')
def home():
    return render_template('index.html')

def split_row_into_cells(row):
    return [cell.strip() for cell in row.split('|') if cell.strip()]

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    idx = data.get('idx')
    text = data.get('text')

    if idx == '1':
        output = generate_title(text)
    elif idx == '2':
        output = generate_content(text)
    else:
        return jsonify({"error": "Invalid idx value"}), 400

    try:
        # Each row should start with "| " and end with " |". Split by '\n' and strip leading/trailing whitespaces.
        rows = [row.strip() for row in output.split('\n') if row.strip().startswith("|") and row.strip().endswith("|")]

        # Each cell is surrounded by " | ", so split by that. Skip the first and last cell of each row because they are empty.
        table = [split_row_into_cells(row) for row in rows]

        return jsonify({"output": table})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
