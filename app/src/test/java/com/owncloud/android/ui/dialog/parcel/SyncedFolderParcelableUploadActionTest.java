/*
 * Nextcloud - Android Client
 *
 * SPDX-FileCopyrightText: 2026 RPA4All contributors
 * SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-only
 */
package com.owncloud.android.ui.dialog.parcel;

import com.nextcloud.client.jobs.upload.FileUploadWorker;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class SyncedFolderParcelableUploadActionTest {

    @Test
    public void setUploadActionDeleteMapsToDeleteBehaviour() {
        SyncedFolderParcelable parcelable = new SyncedFolderParcelable();

        parcelable.setUploadAction("LOCAL_BEHAVIOUR_DELETE");

        assertEquals(FileUploadWorker.LOCAL_BEHAVIOUR_DELETE, (int) parcelable.getUploadAction());
        assertEquals(2, (int) parcelable.getUploadActionInteger());
    }

    @Test
    public void setUploadActionForgetMapsToDefaultBehaviour() {
        SyncedFolderParcelable parcelable = new SyncedFolderParcelable();

        parcelable.setUploadAction("LOCAL_BEHAVIOUR_DELETE");
        parcelable.setUploadAction("LOCAL_BEHAVIOUR_FORGET");

        assertEquals(FileUploadWorker.LOCAL_BEHAVIOUR_FORGET, (int) parcelable.getUploadAction());
        assertEquals(0, (int) parcelable.getUploadActionInteger());
    }
}
