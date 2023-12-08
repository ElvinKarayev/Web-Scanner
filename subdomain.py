import asyncio
import aiohttp
import pyfiglet

ascii_txt = """"
                                                ......                                              
                                        :7YPBBBBBBBBBBB#BBPY7^.                                     
                                   .!P##B57^..           .^75B##P!.                                 
                                .J#&P!.        ..    :..       .!G&#J.                              
                              ~B&5^  .:~7YG#&&@@B    @@@@~   ~^.   ^B@G                             
                            ?&@@BB&@@@@@@@&#G@@@G    @@@@!   &@@@7   &@BJJ                          
                          ~&@@@@@&B5?&@@B    &@@@PGPG@@@@B!^:&@@@7  .@@@@@&~                        
                         G@Y.@@@&    G@@G    #@&@@@@@@@@@@@@@@@@@#J!?@@@@:7@G                       
                       .&@~ .@@@&    G@@G           .@@@@@@@@@@@@@@@@@@@@G :&&.                     
                      .&@:  .@@@&    G@@G            @@@@@@@@@@@@@@@@@@@@#7  &@.                    
                      #@:   .@@@&    G@@G        :~7?YPG#@@@@@@@@@@@@@@@@7.  .@&                    
                     ?@?    .@@@&    G@@G    .J#@@@@@     :J&@@@@@@@@@@@@:    ~@J                   
                     @&     .@@@&    G@@G  .G@@@&P7^:        ~&@@@@@@@@@@:     #@.                  
                    ~@Y     .@@@&    G@@G :@@@#^               G@@@@@@@@@:     !@!                  
                    J@~     .@@@&    G@@G @@@B    ?B&&#?        &@@@@@@@@:     :@5                  
                    Y@^     .@@@&    B@@@&@@@.   B@@@@@@#       J@@@@@@@@:     .@G                  
                    ?@~     .@@@&    J###&@@@.   B@@@@@@#       J@@@@@@@@.     ^@Y                  
                    :@P     .@@@@.        &@@B    7B&&B?        &@@@@@@@&      J@~                  
                     #@.     #@@@J        :@@@&~               B@@@@@@@@!      &&                   
                     ^@P     ^@@@@.        .P@@@&G?~^        !&@@@@@@@@P      J@!                   
                      Y@7     7@@@&.         G@@@@@@@     ^Y&@@@@@@@@@P      ~@P                    
                       G@!     ?@@@@~        P@@B.^!75PB&@@@@@@@@@@@@?      ~@G                     
                        5@Y    ^P@@@@P       P@@G    @@@@@@@@@@@@@@B.      J@Y                      
                         ~@&:  .?@@@@@@J     P@@G    @@@@@@@@@@@@#^      :#@~                       
                           P@G.  :@&!#@@@Y.  P@@G    @@@@@@@@@@#^      .P@5                         
                            :G@B^ 7@Y ^B@@@5.P@@B    @@@@@@@@B^      ^G&5.                          
                              .Y&&?P@5  :G@@@@@@B    @@@@@@B^     :Y##7                             
                                 ^Y7?&&J. .Y@@@@G    &@@@B:   :7P#B?.                               
                                      ^PBBGY5&@@#...:@@@G?JPGGP?^                                   
                     ..     ..  ..   .    .^?5P5PPGPB#BJ7!!!^     ......    ...                     
                     &@@J !@@@..@@^ P@B     5@P     5@G .G@&@@G. Y@@@@@&  5@@@@#~                   
                     &@@@@@@@@..@@~ G@B     G@B     P@B &@G  G@& 5@&     5@&. ?@@.                  
                     &@?~&?~@@..@@~ G@B     G@B     P@B 5@&7.^Y7 5@&?777 G@B   ::                   
                     &@?   ^@@..@@~ G@B     G@B     P@B  :5&@&Y. 5@@#B#B P@B                        
                     &@?   ^@@..@@~ G@B     G@B     P@B GB~ .B@& 5@#     G@B  .B#.                  
                     @@?   ^@@..@@~ B@@PPPY B@@PPPY G@# 5@@5Y@@Y P@@PPP5 ~@@GY&@#                   
                     J5:   .5Y  Y5. !5555PY !5555PY ~57  :JGGJ:  ~5555PY  .?PGY^                    

"""
print("\033[94m" + ascii_txt)

MAX_CONCURRENT_REQUESTS = 10  


async def fetch(session, semaphore, sub, target_domain):
    url = f"http://{sub}.{target_domain}"
    try:
        async with semaphore, session.get(url) as response:
            if response.status == 200:
                print("\033[92mValid domain:\033[0m", url)
                print("\033[90mStatus:200\033[0m")
            elif response.status == 401:
                print("\033[92mValid domain:\033[0m", url) 
                print("\033[90mStatus:401\033[0m")
    except aiohttp.ClientError:
        pass


async def enumerate():
    target_domain = input("\033[93mDomaini girin (e.g., example.com):\033[0m ").strip()

    sub_list = open("./sub_wordlists.txt").read()
    subs = sub_list.splitlines()

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, semaphore, sub, target_domain) for sub in subs]
        await asyncio.gather(*tasks)

def main():
    asyncio.run(enumerate())


    