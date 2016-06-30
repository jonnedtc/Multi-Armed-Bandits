import sys
import numpy as np
from Bandits import MeanSample, LinearSample
sys.path.append('../')

from aiws import api
api.authenticate('bandits-of-the-west','')
    
def test_random_requests():
    for run_id in range(5000,5010):

        cumulative_reward = 0
        n = 10000
        
        os_dict = {'Windows':0, 'OSX':0, 'Android':1, 'iOS':1, 'Linux':0}
        referrer_dict = {'Google':0, 'Bing':1, 'Other':1}
        agent_dict = {'Mozilla Firefox':0, 'Google Chrome':0, 'Safari':0, 'Opera':0, 'Internet Explorer':1}
        
        all_header = [5, 15, 35]
        all_language = ['NL', 'EN', 'GE']
        all_adtype = ['skyscraper', 'square', 'banner']
        all_color = ['green', 'blue', 'red', 'black', 'white']
        all_price = map(lambda x: 20+float(x)*2,range(16))
        
        B_header = MeanSample(num_options=len(all_header))
        B_adtype = MeanSample(num_options=len(all_adtype))
        B_color = MeanSample(num_options=len(all_color))
        # num_variables = price + age + os + referrer + agent = 5
        B_price = LinearSample(num_variables = 5)
        
        for request_number in xrange(n):

            # Get context
            context = api.get_context(run_id, request_number)
            error = context['error']
            context = context['context']
            
            # MeanBandits
            choice_header = B_header.recommend()
            choice_adtype = B_adtype.recommend()
            choice_color = B_color.recommend()
            
            # LinearBandit
            best_reward = 0
            best_price = 0
            for price in all_price:
                variables = [price] + [context['age']] + [os_dict[context['os']]] + [referrer_dict[context['referrer']]] + [agent_dict[context['agent']]]
                reward = B_price.recommend(variables) * price
                if reward > best_reward:
                    best_reward = reward
                    best_price = price
            
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
            offer['price'] = best_price
            
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
            
            variables = [best_price] + [context['age']] + [os_dict[context['os']]] + [referrer_dict[context['referrer']]] + [agent_dict[context['agent']]]
            B_price.update(variables, result['success'])

        mean_reward = cumulative_reward / n
        print "Mean reward: %.2f euro" % mean_reward

if __name__ == "__main__":
    test_random_requests()
