@{
from tqdm import tqdm
}
0123456789
-- Answer the following questions about the code snippet below.
                        /*这个也支持
这个是C的多行注释
牛逼吧*/        
<!--这个是html注释


-->

@{count=1}
@{dict2 = {1:"1212", 2:"3asx"}}
@for(index, item in tqdm(self.incontext_samples))
{
-- Question @(index+1)       # 这是注释
# 这也是注释
# 这还是注释

Question: Write a @(item["lang"]) program that prints "Hello World!" to the console. 
Code: @(item["code"]) (@@(item["code"]))
目前的count： @(count)                  
    @if (count >= 2)
    {
> 2!
    }
    @elif (count < 0) {
    < 0???
    }
    @elif (count == 0) {
== 0
    }
    @else
    {
nothing
    }
@{count+=1}
}
    
-- Question @(item["count"])
@while(count > 0)
{
@(count)
@{count -= 1}
@(count+2)
}

Question: Write a @(query_samples['lang']) program that prints "Hello World!" to the console.
Code: