# Spotify API Reference

This document provides a summary of the Spotify API endpoints used in this project.

## [Get User's Saved Tracks](https://developer.spotify.com/documentation/web-api/reference/get-users-saved-tracks)

Get a list of the songs saved in the current Spotify user's 'Your Music' library.

### Authorization Scopes

- `user-library-read`

### Request Parameters

| Name     | Type    | Description                                                                                                                                     |
| -------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `market` | string  | _Optional_. An ISO 3166-1 alpha-2 country code. If a country code is specified, only content that is available in that market will be returned. |
| `limit`  | integer | _Optional_. The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.                                                        |
| `offset` | integer | _Optional_. The index of the first item to return. Default: 0 (the first item). Use with `limit` to get the next set of items.                  |

### Response Body

The response is a [Paging Object](https://developer.spotify.com/documentation/web-api/reference/#object-pagingobject) containing [Saved Track Objects](https://developer.spotify.com/documentation/web-api/reference/#object-savedtrackobject).

#### Saved Track Object

| Name       | Type                                                                                              | Description                            |
| ---------- | ------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `added_at` | string                                                                                            | The date and time the track was saved. |
| `track`    | [Track Object](https://developer.spotify.com/documentation/web-api/reference/#object-trackobject) | Information about the track.           |

## Stats

https://stats.fm/
