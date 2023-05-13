-- Answer the following questions about the code snippet below.

@{count=1}
@{dict2 = {1:"1212", 2:"3asx"}}
@for(index, item in self.incontext_samples)
-- Question @(index+1) # 这是注释
# 这也是注释
# 这还是注释

Question: Write a @(item["lang"]) program that prints "Hello World!" to the console.
Code: @(item["code"]) (@@(item["code"]))
目前的count： @(count) \
    @if(count >= 2)
> 2!
    @elif(count < 0)
< 0???
    @end     
@{count+=1}
@end
-- Question @(item["count"])

Question: Write a @(query_samples['lang']) program that prints "Hello World!" to the console.
Code: