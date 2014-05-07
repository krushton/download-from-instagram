import urllib,urllib2,os,sys
import json,time

images = []

def load_from_instagram(tag, total=20):
        counter = total
	url = 'https://api.instagram.com/v1/tags/' + tag + '/media/recent'
	params = {'client_id' : 'YOUR_CLIENT_ID_HERE'}
	done = False
	print 'Begin processing images, output will be in results folder'
	while (done == False):
                results = call_api(url, params)
                data = results['data']
                for item in data:
                        
                        image_url = item['images']['standard_resolution']['url']
                        image_id = item['id']
                        try:
                                source = item['caption']['from']['username']
                        except:
                                source = ''
                                
                        if not os.path.exists('results'):
                            os.makedirs('results')
                            
                        path = 'results/' + str(image_id) + '.jpg'
                        f = open(path,'wb')
                        f.write(urllib.urlopen(image_url).read())
                        f.close()
                        image = { 'temp_path' : path, 'original_url': image_url, 'source' : source }
                        #can add more metadata here later, right now just grabs file path, url, source
                        images.append(image)
                        counter = counter - 1
                        if counter == 0:
                                done = True
                                break
                        elif counter % 3 == 0:
                                print str(counter) + ' of ' + str(total) + ' images remaining'
                                
                if counter > 0:
                        try:
                                url = results['pagination']['next_url']
                                print 'Making another call to the API for more results'
                                #don't want to hammer the api, wait 2 seconds between requests.
                                time.sleep(2)
                                
                        except:
                                done = True

        print 'Successfully downloaded: ' + str(len(images)) + ' images'
        


#helper functons -------------------------------------------------------------------
def call_api(url,params):
	data = urllib.urlencode(params)
	url = url + '?' + data
	req = urllib2.Request(url)
	result = json.loads(urllib2.urlopen(req).read())   #returns a Python dict of the JSON
	return result


if __name__ == '__main__':
    try:
        hashtag = sys.argv[1]
    except IndexError:
        print 'Usage: download.py <tag> <num of images requested>'
        
    if len(sys.argv) >= 3:
        num_photos = int(sys.argv[2])
        load_from_instagram(hashtag, total=num_photos)
    else:
        load_from_instagram(hashtag)

