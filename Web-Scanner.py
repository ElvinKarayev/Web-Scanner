import os
import requests
import subdomain
import directoryEnum
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
print("\033[94m" + ascii_txt+"\33[0m")


print("\033[91mHansini islətmək istiyirsiz?\033[0m")
print("""\033[92m1.Directory Enumeration
2.SubDomain Enumeration""")
user_choice=int(input("burda qeyd eləyin->\033[0m "))
if (user_choice==1):
    domain=input("Domaini girin (e.g., example.com): ")
    directory_file=open(input("Directorylerin olduğu listin yerini girin (e.g., /usr/share/dict/wordlist-probable.txt): ")).read()
    rate=int(input("directorylerin yoxlanilmasini hansi suretde istiyirsiz?(e.g., 3) Note: 20 den yuxari secseniz avtomatik 20 e dusecey\nbura qeyd edin -> "))
    if (rate>20):
        rate = 20
    elif (rate<1):
        rate=1
    directories=directory_file.splitlines()
    found_directories=directoryEnum.Enumerate(domain,directories,rate)
    if (not found_directories):
        print("Directoryler tapilmadi")
    else:
        os.system("cls")
        for url, status in found_directories:
            print("\033[94m-----------------------------------------------")
            print(f"URL: {url}, Status Code: {status}")
            print("-----------------------------------------------\033[0m")
elif(user_choice==2):
    subdomain.main()