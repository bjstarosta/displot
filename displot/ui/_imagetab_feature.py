# -*- coding: utf-8 -*-
"""displot - Image tab feature marker UI functionality.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

from displot.io import DisplotDataFeature
from ._imageview_symbols import FeatureMarker, FeatureMarkerMini


class ImageTabFeature(DisplotDataFeature):
    """Subclass adding UI functionality to the DisplotDataFeature struct.

    Args:
        itab (ui.ImageTab): Parent ImageTab object.

    Attributes:
        color (QtGui.QColor): Current colour of the feature marker.
        itab

    """

    def __init__(self, itab, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.itab = itab

        self.imViewRef = None
        self.miniViewRef = None

        self.color = self.itab.window.styles.defaultColour
        self._prevColor = None

        self.isDrawn = False
        self.isHighlighted = False
        self.isSelected = False
        self.isHidden = False

    def fromParent(self, obj):
        """Populate the current object using a base class object instance.

        Args:
            obj (io.DisplotDataFeature): Base class object.

        Returns:
            None

        """
        for attr, value in obj.__dict__.items():
            setattr(self, attr, value)

    def toParent(self):
        """Return the current object as its base object type.

        Transfers all attributes set in this object that als exist in the
        parent.

        Returns:
            io.DisplotDataFeature: Data object.

        """
        obj = DisplotDataFeature()
        for attr, value in obj.__dict__.items():
            setattr(obj, attr, getattr(self, attr))
        return obj

    def show(self):
        """Show the feature in the GUI if its hidden or not drawn.

        Returns:
            None

        """
        if self.isDrawn is False:
            self.update()
        self.imViewRef.show()
        self.miniViewRef.show()
        self.isHidden = False

    def hide(self):
        """Hide the feature in the GUI.

        Returns:
            None

        """
        self.imViewRef.hide()
        self.miniViewRef.hide()
        self.isHidden = True

    def select(self, toggle=True):
        """Select the feature in the GUI.

        Args:
            toggle (bool): True selects the feature, False unselects it.

        Returns:
            None

        """
        if toggle is True:
            self.highlight(True)
            self.isSelected = True
        else:
            self.isSelected = False
            self.highlight(False)

    def highlight(self, toggle=True):
        """Highlight the feature in the GUI.

        This only affects the QGraphicsView objects, and not the QTableView
        the feature is associated with.

        Args:
            toggle (bool): True highlights the feature, False unhighlights it.

        Returns:
            None

        """
        if self.isSelected is True:
            return

        if toggle is True:
            self._prevColor = self.color
            self.color = self.itab.window.styles.highlightColour
            self.isHighlighted = True

        else:
            if self._prevColor is not None:
                self.color = self._prevColor
                self._prevColor = None
            self.isHighlighted = False

        self.update()

    def move(self, x, y):
        """Move feature to new coordinates on the image.

        Args:
            x (int): X component of the new coordinates.
            y (int): Y component of the new coordinates.

        Returns:
            None

        """
        self.x = x
        self.y = y

        self.update()

    def centerOn(self):
        """Center the working image view on the feature.

        Returns:
            None

        """
        self.itab.imView.centerOn(self.imViewRef)

    def removeFromScene(self):
        """Remove the feature from its associated QGraphicsScene objects.

        Note: This does not affect any data objects the feature may be
        contained in, so calling this without cleaning up remaining references
        to this object will result in a feature that is invisible in the UI.

        Returns:
            None

        """
        if self.imViewRef is not None:
            self.itab.imView.removeGraphicsItem(self.imViewRef)
            self.imViewRef = None
        if self.miniViewRef is not None:
            self.itab.miniView.removeGraphicsItem(self.miniViewRef)
            self.miniViewRef = None

    def update(self):
        """Update the QGraphicsScene objects meant to hold this feature.

        This will create new scene references for the feature, and so should
        be called after feature creation to place it in the scene.

        Returns:
            None

        """
        if self.imViewRef is None:
            self.imViewRef = FeatureMarker()
            self.itab.imView.addGraphicsItem(self.imViewRef)
        if self.miniViewRef is None:
            self.miniViewRef = FeatureMarkerMini()
            self.itab.miniView.addGraphicsItem(self.miniViewRef)

        pred_colour = self.itab.window.styles.cmap(self.confidence)

        self.imViewRef.setTextValue('{:.3f}'.format(self.confidence))
        self.imViewRef.penNormal.setColor(pred_colour)
        # self.imViewRef.penNormal.setColor(self.color)
        self.imViewRef.update()
        self.imViewRef.setPos(
            self.x - self.imViewRef.width / 2,
            self.y - self.imViewRef.height / 2
        )

        self.miniViewRef.penNormal.setColor(pred_colour)
        # self.miniViewRef.penNormal.setColor(self.color)
        self.miniViewRef.update()
        scale = self.itab.miniView.getMinimapRatio()
        self.miniViewRef.setPos(
            (self.x * scale) - self.miniViewRef.width / 2,
            (self.y * scale) - self.miniViewRef.height / 2
        )

        self.isDrawn = True
