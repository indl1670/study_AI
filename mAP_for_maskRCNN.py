import os

def compute_batch_ap(image_ids):
    APs = []
    count = 0
    for image_id in image_ids:
        count+=1
        print(f"진행률: {count}/{len(image_ids)}")
        results = model.detect([image], verbose=0)
        # Compute AP
        r = results[0]
        AP, precisions, recalls, overlaps =\
            utils.compute_ap(gt_bbox, gt_class_id, gt_mask,
                              r['rois'], r['class_ids'], r['scores'], r['masks'])
        APs.append(AP)
        print("mAP @ IoU=50: ", np.mean(APs))
    return APs

test_list = [i for i in dataset.image_ids]
image_ids = np.array(test_list)

APs = compute_batch_ap(image_ids)
print("mAP @ IoU=50: ", np.mean(APs))