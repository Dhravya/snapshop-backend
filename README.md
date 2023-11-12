
## Inspiration

As tech enthusiasts, we constantly faced the dilemma: _**What to wear?**_ and _**Do I look on point?**_ These questions resonate with many teenagers who, influenced by celebrities and peers with sharp fashion senses, may struggle with self-doubt. Moreover, staying trendy doesn't come cheap, and scouring for the best deals on the latest fashion is a challenge in itself. 
And buying isn't simple - **would it look good on me?** is always a question we have. 

That's where SnapShop comes in—an intelligent assistant designed to address your fashion queries.

Our personal experiences, like attending hackathons unprepared for the weather or dress code, highlighted the need for a solution. We recall a time at Calhacks where our lack of preparation led us to seek warmth sleeping near a bathroom (and getting woken up by the security)! SnapShop aims to prevent such fashion faux pas by providing weather-appropriate and event-specific style advice, ensuring you feel confident and appropriately dressed for any occasion, while keeping the bills bearable.


## What it does
#### Click an image to Shop: 
SnapShop recognizes all the fashion items in the image and tells you what YOU need to buy, to get exactly the same look at the best deals.

Basicaly, image -> best shopping links
[demo link]

#### Ask a query
Say you don't know much about the outfit style you want to go with, for an event
You can ask questions like _**"I'm going to Mumbai, India for a wedding. It's a Gujarati family. I don't want to overdress. What should I wear?"**_
And voila, shopwise will generate a list of ethnic wear you should consider buying.
... or **"There's a tech meetup in San Fransisco. The meetup is about AI, I don't know if I should wear formal. I'm going next week. "**_ (Sent in November)
SnapShop recognises that San Fransisco will be really cold, and that techies usually wear plain t-shirts.

So, it recommends **semi-formal**- buying plain t-shirts and a zip-up jacket, and a pant.
![it works!](https://i.dhr.wtf/r/Clipboard_Nov_12,_2023_at_7.33 AM.png)

Another prompt: 
I'm going to mumbai in the summer, what should I wear?
![it works!](https://i.dhr.wtf/r/Clipboard_Nov_12,_2023_at_7.32 AM.png)

#### TRY IT ON ME
Users can also try clothes on themselves! 
(... Update: Disabled, too costly to run/test)

#### Explore page
On the explore page, users can easily find good deals found by other users.

## How we built it

Here's the tech stack we used:
- OpenAI's new **Vision**
- **ShopWise * API** that we built for scraping the web to get the best prices for products
- **Flutter** for the Mobile app
- **FastAPI** for python backend
- **Redis**, hosted on Redis Cloud (As DB)
- A Cloudflare Worker as a proxy for Verbwire API
- **VerbWire** to store images on blockchain
- **Firebase** for user authentication

![Our infrastructure](https://i.dhr.wtf/r/infra.jpeg)

With this infrastructure, we still manage to get really fast response times - evern with image and web scraping, we can get perfect response in less than 30 seconds. 

## Challenges we ran into
It was really difficult to implement the Vision part effectively, and get the output data in a certain format so that we can properly parse it (Since the vision API doesn't support function calls)

And ofcourse, the indexing and web search part was especially complex. Getting it to work was very, very challenging, as finding the best deals from all over the internet is a very difficult task.

## Accomplishments that we're proud of
We are really proud of making something that we would actually use in our daily lives. Finding the best deals and being fashionable is a real problem that both of us face. Also, the fact that we completed the entire thing, and got it to work, while making it look good and usable is quite the feat.

## What we learned
We learnt a lot from SnapShop. A very important thing that we realised was time management and it's importance in hackathons. Also, we realised that we didn't take pricing into consideration, and after building the try it on me feature, we realised that it was wayyy too expensive to run for us.

## What's next for SnapShop
In the future, we want to make snapshop into a full consumer product. Because we really believe in the idea, we think that monetizing the app wouldn't be that big of a challenge. 
