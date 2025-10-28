import OpenAI from "openai";
import * as dotenv from "dotenv";

dotenv.config();

/**
 * Calculates the cosine similarity between two vectors.
 * @param vector1 The first vector.
 * @param vector2 The second vector.
 * @returns The cosine similarity score.
 */
function cosineSimilarity(vector1: number[], vector2: number[]): number {
    if (vector1.length !== vector2.length) {
        throw new Error("Vector dimensions must match for cosine similarity calculation.");
    }

    const dotProduct = vector1.reduce((acc, val, index) => acc + val * vector2[index], 0);
    const magnitude1 = Math.sqrt(vector1.reduce((acc, val) => acc + val ** 2, 0));
    const magnitude2 = Math.sqrt(vector2.reduce((acc, val) => acc + val ** 2, 0));

    if (magnitude1 === 0 || magnitude2 === 0) {
        throw new Error("Magnitude of a vector must be non-zero for cosine similarity calculation.");
    }

    return dotProduct / (magnitude1 * magnitude2);
}

/**
 * Main function to execute the document similarity comparison.
 */
async function main() {
    try {
        
        console.log("== Building Search Applications with OpenAI ==");

        const client = new OpenAI();
        const model = "text-embedding-3-small"; // here should be of type ADA embedding for OpenAI

        const source = "Car";
        const compareTo = "Vehicle";
        const parrot = "A bird";

        const embeddings = await client.embeddings.create({
            model: model,
            input: [source],
            encoding_format: "float",
        });

        const parrotEmbedding = await client.embeddings.create({
            model: model,
            input: [parrot],
            encoding_format: "float",
        });

        const embeddingsCompareTo = await client.embeddings.create({
            model: model,
            input: [compareTo],
            encoding_format: "float",
        });

        // console.log("Parrot Embeddings response:", parrotEmbedding.data[0].embedding);
        // console.log("CompareTo Embeddings response:", embeddingsCompareTo.data[0].embedding);
        // console.log("Embeddings response:", embeddings.data[0].embedding);

        const carArray = embeddings.data[0].embedding;
        const vehicleArray = embeddingsCompareTo.data[0].embedding;
        const parrotArray = parrotEmbedding.data[0].embedding;

        const scoreCarWithCar  = cosineSimilarity(carArray, carArray);
        console.log("Comparing - Car vs Car...: ", scoreCarWithCar.toFixed(7));

        const scoreCarWithVehicle  = cosineSimilarity(carArray, vehicleArray);
        console.log("Comparing - Car vs Vehicle...: ", scoreCarWithVehicle.toFixed(7));

        const scoreCarWithParrot  = cosineSimilarity(carArray, parrotArray);
        console.log("Comparing - Car vs Parrot...: ", scoreCarWithParrot .toFixed(7));

    } catch (error) {
        console.error("The sample encountered an error:", error);
    }
}

main();