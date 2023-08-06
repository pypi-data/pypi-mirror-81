# **Introduction**

This is a Program which can **simulate** EMOTIONS and MOOD.                      
*This contains of the following Units:*---


> -   **Essential Information:**
    *This contains some essential snippets for core processing etc.*
*   **Knowladge Input:** 
    *Here the System processes and stores the Data in its ONLINE DATABASE.*
*   **Get Value:**
    *This fetches the value from the ***knowladge*** Database and is prossesed by removing unnecessary **" , "** and " [ , ] " for furthur processing if the data in **Mood** and **Emotion** part.* 
*   **Mood of the System:**
    *Here the System calculates its ***Mood*** from its Database.*
*   **Refine Input:**
    *As the Data is stored in a unique format in the Database, it is Decoded here.*
*   **Processing:**
    *Here the System calculates its ***Emotion*** from its Database.*
*   **Output:**
    *This is the final output or the status of imotion of the System.*


**_____________________________________________________________**
**__________________________________**
### **Installation**
To use `emotions`, you need to have the package installed.

    $ sudo pip install emotions





### **Usage**


**Here are some set of commands to use it in Projects.** This module can be very effective for Projects like Personal assistants
> - ```import emotions as aE```: For Importing the module as ```aE```.
> - ```aE.emotion(ask)```:  Here ```ask=``` The word you want the **AI** to react to. Note that the **Mood** of AI is independent.
> - ```aE.learn(input, emotion, url)```:  It is used to teach the **AI** about different **words** and our **feeling** about them. Here input refers to the **words**, emotion refers to the  **feeling** and `url` reffers to the *url* of the **Firebase Database**.  Once the **information** is stored it prints `'Got it!'`.Note that if your firebase database has no bucket `'/count'` it will **not work**. So first go ahead and create a `'/count'`  and store value `0` with tag `/1`
> - To `print()` the out put, `print(aE.mood)`: to print the **Mood** and `print(aE.feelings)`: to print the **Emotion.**