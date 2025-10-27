import OpenAI from "openai";
import * as dotenv from "dotenv";

dotenv.config();

export async function main() {
    try {
        console.log("== Chat Completions App ==");

        // const client = new OpenAIClient(endpoint, new AzureKeyCredential(azureApiKey));
        const client = new OpenAI({
            apiKey: process.env['OPENAI_API_KEY'], // This is the default and can be omitted
        });

        const deploymentName = 'gpt-5-nano';
        // const deploymentName = '<include-your-deployment-name-here>';

        // const result = await client.responses.create({
        //     model: deploymentName,
        //     instructions: "You are the president of France. You have just resigned.",
        //     input: "Write a speech (in English) to the nation explaining your decision.",
        // });

        // console.log(result.object);
        // console.log(result.output);
        // console.log(result.output_text);

        const stream = await client.responses.stream({
            model: deploymentName,
            instructions: "You are the president of France. You have just resigned.",
            input: "Write a speech (in English) to the nation explaining your decision.",
            reasoning: {
                effort: "minimal",
            }
        });

        for await (const event of stream) {
        //    console.log(event);
            if (event.type === 'response.output_text.delta') {
                process.stdout.write(event.delta);
            }
        }

        
    } catch (error) {
        console.log("The sample encoutered an error: ", error);
    }
}

main();