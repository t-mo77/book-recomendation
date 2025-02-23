
2/teamspace/studios/this_studio/gradio-dashboard.py�import pandas as pd
import numpy as np
import gradio as gr
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.vectorstores import Chroma

books=pd.read_csv("books_with_emotions.csv")
books["large_thumbnail"] = books["thumbnail"]+"&fife=w800"
books["large_thumbnail"] = np.where(
    books["large_thumbnail"].isna(),
    "cover-not-found.jpg",
    books["large_thumbnail"]
)


model_name = "intfloat/multilingual-e5-base"
model_path = f"path_to_model/{model_name}"
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name=model_path)

raw_documents = TextLoader("tagged_descriptions.txt").load()
text_splitter=CharacterTextSplitter(chunk_size=0, chunk_overlap=0,separator="\n")
documents=text_splitter.split_documents(raw_documents)
db_books=Chroma.from_documents(documents, embeddings)


def retrieve_semantic_recommendations(
        query: str,
        category: str = None,
        tone: str = None,
        initial_top_k: int = 50,
        final_top_k: int = 16,
) -> pd.DataFrame:

    recs = db_books.similarity_search(query, k=initial_top_k)
    books_list = [int(rec.page_content.strip('"').split(":")[0]) for rec in recs]
    book_recs = books[books["isbn13"].isin(books_list)].head(initial_top_k)

    if category != "All":
        book_recs = book_recs[book_recs["simple_categories"] == category].head(final_top_k)
    else:
        book_recs = book_recs.head(final_top_k)

    if tone == "Happy":
        book_recs.sort_values(by="joy", ascending=False, inplace=True)
    elif tone == "Surprising":
        book_recs.sort_values(by="surprise", ascending=False, inplace=True)
    elif tone == "Angry":
        book_recs.sort_values(by="anger", ascending=False, inplace=True)
    elif tone == "Suspenseful":
        book_recs.sort_values(by="fear", ascending=False, inplace=True)
    elif tone == "Sad":
        book_recs.sort_values(by="sadness", ascending=False, inplace=True)

    return book_recs


def recommend_books(
        query: str,
        category: str,
        tone: str
):
    recommendations = retrieve_semantic_recommendations(query, category, tone)
    results = []

    for _, row in recommendations.iterrows():
        description = row["description"]
        truncated_desc_split = description.split()
        truncated_description = " ".join(truncated_desc_split[:30]) + "..."

        authors_split = row["authors"].split(";")
        if len(authors_split) == 2:
            authors_str = f"{authors_split[0]} and {authors_split[1]}"
        elif len(authors_split) > 2:
            authors_str = f"{', '.join(authors_split[:-1])}, and {authors_split[-1]}"
        else:
            authors_str = row["authors"]

        caption = f"{row['title']} by {authors_str}: {truncated_description}"
        results.append((row["large_thumbnail"], caption))
    return results

categories = ["All"] + sorted(books["simple_categories"].unique())
tones = ["All"] + ["Happy", "Surprising", "Angry", "Suspenseful", "Sad"]

with gr.Blocks(theme = gr.themes.Glass()) as dashboard:
    gr.Markdown("# Semantic book recommender")

    with gr.Row():
        user_query = gr.Textbox(label = "Please enter a description of a book:",
                                placeholder = "e.g., A story about forgiveness")
        category_dropdown = gr.Dropdown(choices = categories, label = "Select a category:", value = "All")
        tone_dropdown = gr.Dropdown(choices = tones, label = "Select an emotional tone:", value = "All")
        submit_button = gr.Button("Find recommendations")

    gr.Markdown("## Recommendations")
    output = gr.Gallery(label = "Recommended books", columns = 8, rows = 2)

    submit_button.click(fn = recommend_books,
                        inputs = [user_query, category_dropdown, tone_dropdown],
                        outputs = output)


if __name__ == "__main__":
    dashboard.launch()
 0*$e77df05a-9736-4484-a396-81bf5a723f09082; *$470c71a4-b213-4a15-9e07-cc6c74354e6908;DDS0Sv*$27ef09dc-94d7-431a-a6ae-a6536efcb3c5083v� *$db1559a9-a3b8-45a1-bbae-4615b6cca51008
�� 4�� *$a127cdee-b307-4ec2-88a9-3207f261919b08
�� 4�� *$751d9a12-0e5b-4fae-837b-4f00a04c2f2f084�� *$a127cdee-b307-4ec2-88a9-3207f261919b08
�� 2��*$aeb5592e-7ff4-4d9f-afba-0b53f6a5e9b608
�� 4�� *$aeb5592e-7ff4-4d9f-afba-0b53f6a5e9b608
�� 2��*$2a2fc271-e1e0-40e8-b34d-fb32737eb64c08
�� 4�� *$2a2fc271-e1e0-40e8-b34d-fb32737eb64c08
�� 4�� *$8731cf91-5e8e-432b-ae7e-83cc9e3352e508��4�� *$8731cf91-5e8e-432b-ae7e-83cc9e3352e508
�� 2��*$9100c493-5c94-40c5-a6dd-98f01be8b3bd08
�� 2��*$9100c493-5c94-40c5-a6dd-98f01be8b3bd08
�� 2��*$a77ed2f8-fd2d-460c-939a-6cbcb4e70f7708
�� 
�� 
�� 2��*$1b4a7907-6b36-4346-aa28-b1dc33ba1666084�� *$1b4a7907-6b36-4346-aa28-b1dc33ba166608��4�� *$5e12988f-971c-45a5-9fe1-2bd4d1ed81b308
�� 
��	 
�	�	 
�	� 
�� 29file:///teamspace/studios/this_studio/gradio-dashboard.py