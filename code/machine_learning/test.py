import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image

# Load the pre-trained ResNet50 model
model = resnet50(pretrained=True)
model.eval()
print(model)

# Define the image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load the class labels
with open("food_labels.txt") as f:
    labels = f.read().splitlines()

# Define a function to preprocess the input image
def preprocess_image(image):
    image = transform(image).unsqueeze(0)
    return image

# Define a function to classify the image
def classify_image(image_path):
    # Load and preprocess the image
    image = Image.open(image_path).convert("RGB")
    preprocessed_image = preprocess_image(image)

    # Make predictions on the preprocessed image using the ResNet50 model
    with torch.no_grad():
        outputs = model(preprocessed_image)
    _, predicted_idx = torch.max(outputs, 1)

    # Get the predicted class label
    predicted_label = labels[predicted_idx.item()]

    return predicted_label

# Example usage
image_path = "meal.jpg"
predicted_label = classify_image(image_path)
print("The food is classified as:", predicted_label)
