import sys
import numpy as np
from Bandits import SampleBandit
sys.path.append('../')

from aiws import api
api.authenticate('bandits-of-the-west','')
    
def test_random_requests():
    for run_id in range(5000,5010):

        cumulative_reward = 0
        n = 10000
        
        all_header = [5, 15, 35]
        all_language = ['NL', 'EN', 'GE']
        all_adtype = ['skyscraper', 'square', 'banner']
        all_color = ['green', 'blue', 'red', 'black', 'white']
        all_price = map(lambda x: 20+float(x)*2,range(16))
        
        B_header = SampleBandit(num_options=len(all_header))
        B_adtype = SampleBandit(num_options=len(all_adtype))
        B_color = SampleBandit(num_options=len(all_color))
        B_price = SampleBandit(num_options=len(all_price), weights=all_price)
        
        for request_number in xrange(n):

            # Get context
            context = api.get_context(run_id, request_number)
            error = context['error']
            context = context['context']
            
            # Bandit choice 
            choice_header = B_header.recommend()
            choice_adtype = B_adtype.recommend()
            choice_color = B_color.recommend()
            choice_price = B_price.recommend()
            
            # Create offer
            offer = {
                    'header': all_header,
                    'language': all_language,
                    'adtype': all_adtype,
                    'color': all_color,
                    'price': all_price
                }
            if context['language'] == 'Other':
                offer['language'] = 'EN'
            else:
                offer['language'] = context['language']
            offer['header'] = all_header[choice_header]
            offer['adtype'] = all_adtype[choice_adtype]
            offer['color'] = all_color[choice_color]
            offer['price'] = all_price[choice_price]
            
            result = api.serve_page(run_id, request_number,
                header=offer['header'],
                language=offer['language'],
                adtype=offer['adtype'],
                color=offer['color'],
                price=offer['price'])

            reward = offer['price'] * result['success']
            cumulative_reward += reward
            
            # Save result
            B_header.update(choice_header, result['success'])
            B_adtype.update(choice_adtype, result['success'])
            B_color.update(choice_color, result['success'])
            B_price.update(choice_price, result['success'])

        mean_reward = cumulative_reward / n
        print "Mean reward: %.2f euro" % mean_reward

if __name__ == "__main__":
    test_random_requests()
