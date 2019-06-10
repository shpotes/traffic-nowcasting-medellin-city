import tensorflow as tf

def prepare_dataset(img, model=None, size=(32, 32)):
    if model:
        pass
    else:
        img = tf.image.resize(image, size=size)
        img = image / 255.0
    return img

def build_source_from_metada(metadata_path, data_dir, mode):
    df.read_csv(metadata_path)
    df = df[df['split'] == mode]
    df['filepath'] = df['filename'].apply(lambda x: os.path.join(data_dir, x))

    sources = list(zip(df['filepath'], df['name']))
    return sources

def augment_image(img):
    return img

def load(raw):
    filepath = raw['image']
    img = tf.io.read_file(filepath)
    img = tf.io.decode_jpeg(img)
    return img, raw['label']

def make_dataset(source, training=False, batch_size=1, num_epochs=1,
               num_parallel_calls=1, shuffle_buffer_size=None):
    if not shuffle_buffer_size:
        shuffle_buffer_size = batch_size * 4

    image, labels = zip(*souces)

    ds = tf.data.Dataset.from_tensor_slices({
        'image' : list(image),
        'label' : list(label)
    })

    if training:
        ds.shuffle(shuffle_buffer_size)

    ds = ds.map(load, num_parallel_calls=num_parallel_calls)
    ds = ds.map(lambda x, y: (preprocess_image(x), y))

    if training:
        ds.map(lambda x, y: (augment_image(x), y))

    ds = ds.repeat(count=num_epochs)
    ds = ds.batch(batch_size=batch_size)
    ds = ds.prefetch(1)

    return ds

def imshow_batch_of_three(batch, show_label=True, label_map=None):
    label_batch = batch[1].numpy()
    image_batch = batch[1].numpy()

    if not label_map:
        label_map = list(range(label_batch.max()))

    fig, axarr = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    for i in range(3):
        img = image_batch[i, ...]
        axarr[i].imshow(img)
        if show_label:
            axarr[i].set(xlabel='label = {}'.format(label_map[label_batch[i]]))

def imshow_with_predictions(model, batch, show_label=True, label_map=None):
    label_batch = batch[1].numpy()
    image_batch = batch[0].numpy()

    if not label_map:
        label_map = list(range(label_batch.max()))

    pred_batch = model.predict(image_batch)
    fig, axarr = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

    for i in range(3):
        img = image_batch[i, ...]
        axarr[i].imshow(img)
        pred = int(np.argmax(pred_batch[i]))
        msg = f'pred = {pred}'
        if show_label:
            msg += f', label = {label_map[label_batch[i]]}'
        axarr[i].set(xlabel=msg)