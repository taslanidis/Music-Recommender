# Music Recommender
**Music recommendation system for groups of people.**

⭕ 👤 → 🎶 Music recommendation for individuals has long been ongoing on major platforms such as Spotify and Youtube. 

✅ 👥 → 🎶 The issue at hand is how to deal with recommending music based on a dynamic environment of people entering or leaving a group.

## The Idea
💡 This is a first step in a process of creating an automatic DJ system for private parties, small bars and dedicated clubs where the audience control the music being played based on their suggestions.

Everything is designed around representation vectors for tracks, artists and genres.

## Track Representation Vector
The foundation of the algorithm is the track representation vector.

![TRV](docs/track_representation_vector.png)

## Data
In order to represent the entities accordingly, the data architecture is presented as per below.

![Data](docs/input_data.png)

## Artist Embeddings
Artist embeddings have been created by web scraping Wikipedia. Who other artists have they collaborated with, who they had a concert with, and others that are a simple reference in the same page.

In order to plot them in the 2D space, the TSNE dimensionality reduction algorithm is used.

![ArtistVectors](docs/artist_representation.png)

## Identifying Group Music taste profile

The profile can be identified by one or more vectors that will be later used for recommendations.

In order to do that, all the track representation vector dimensions are reduced with **TSNE**, and then all different music tastes are identified with the **DBSCAN clustering algorithm**.

![2dgraphtracks](docs/2dgraph.png)

**Process:**
1. M clusters from DBSCAN
2. Find the weighted centroid of the cluster based on each users track weight. (This is relevant to how many tracks each user submitted)

![vector_n_space](docs/vector_n_space.jpg)

## Recommendation algorithm

1. The party/bar/club owner can set party settings to finetune results to specific preferences, e.g highly danceable or include only techno and deep house tracks.
2. For each M profile there are K possible matches which will all be filtered based on settings, and the neighbors with the highest scores will be kept.

## Curator

Because different versions of the same tracks exist with the same vectors, a curator has been created that operate as a DJ, that will keep the most relevant version of same tracks, and sort the tracks recommended based on energy and track bpm.

## System
A system has been created with FastAPI that you can just execute and have the backend ready for your application.

There are all the necessary endpoints ready for consumption.

## !!! The only thing missing and I can't post publicly is the library of tracks that I have from SpotifyAPI with audio features
